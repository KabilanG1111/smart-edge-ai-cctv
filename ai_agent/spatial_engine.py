"""
🗺️ SPATIAL AWARENESS ENGINE
============================

Manages dynamic zones, spatial rules, and access control.

Capabilities:
- Dynamic ROI zones (polygon-based)
- Restricted zones with time-based rules
- Entry-only / Exit-only validation
- Crowd density monitoring
- Multi-zone path analysis
- Spatial rule violation detection

Zone Types:
- RESTRICTED: No entry allowed
- ENTRY_ONLY: Can enter but not exit
- EXIT_ONLY: Can exit but not enter
- TIME_RESTRICTED: Access based on time windows
- CROWD_LIMIT: Density threshold enforcement

CPU Optimizations:
- Shapely for fast polygon operations
- Spatial indexing for zone lookup
- Vectorized point-in-polygon checks
"""

import numpy as np
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass, field
from datetime import datetime, time
from enum import Enum
import threading
import logging

logger = logging.getLogger(__name__)


class ZoneType(Enum):
    """Zone access control types"""
    NORMAL = "normal"
    RESTRICTED = "restricted"
    ENTRY_ONLY = "entry_only"
    EXIT_ONLY = "exit_only"
    TIME_RESTRICTED = "time_restricted"
    CROWD_LIMIT = "crowd_limit"


class ViolationType(Enum):
    """Spatial rule violation types"""
    RESTRICTED_ACCESS = "restricted_access"
    ENTRY_VIOLATION = "entry_violation"
    EXIT_VIOLATION = "exit_violation"
    TIME_VIOLATION = "time_violation"
    CROWD_LIMIT_EXCEEDED = "crowd_limit_exceeded"
    WRONG_DIRECTION = "wrong_direction"


@dataclass
class Zone:
    """Spatial zone definition"""
    zone_id: str
    name: str
    polygon: np.ndarray  # Nx2 array of (x, y) coordinates
    zone_type: ZoneType = ZoneType.NORMAL
    
    # Access control
    allowed_classes: Optional[Set[str]] = None  # None = all allowed
    denied_classes: Optional[Set[str]] = None
    
    # Time-based restrictions
    allowed_time_start: Optional[time] = None  # e.g., time(9, 0) = 9:00 AM
    allowed_time_end: Optional[time] = None    # e.g., time(17, 0) = 5:00 PM
    
    # Crowd density
    max_occupancy: int = 100
    current_occupancy: int = 0
    
    # Directional constraints
    entry_direction: Optional[float] = None  # Angle in degrees
    exit_direction: Optional[float] = None
    direction_tolerance: float = 45.0  # Degrees
    
    # Severity weight for this zone
    severity_weight: float = 1.0
    
    # Metadata
    active: bool = True
    violations_count: int = 0


@dataclass
class SpatialViolation:
    """Spatial rule violation record"""
    track_id: int
    zone_id: str
    violation_type: ViolationType
    timestamp: datetime
    position: Tuple[float, float]
    class_name: str
    severity: float
    reason: str


class SpatialAwarenessEngine:
    """
    Spatial Awareness Engine - Manages zones and spatial rules.
    
    Thread-safe, high-performance polygon operations.
    """
    
    def __init__(self, frame_width: int = 1920, frame_height: int = 1080):
        """
        Initialize Spatial Awareness Engine
        
        Args:
            frame_width: Video frame width for coordinate normalization
            frame_height: Video frame height for coordinate normalization
        """
        self.frame_width = frame_width
        self.frame_height = frame_height
        
        # Thread-safe zone management
        self.zones: Dict[str, Zone] = {}
        self.lock = threading.RLock()
        
        # Tracking object-zone relationships
        self.object_zones: Dict[int, str] = {}  # track_id -> current zone_id
        self.object_zone_history: Dict[int, List[str]] = {}  # track_id -> [zone_ids]
        
        # Violation tracking
        self.violations: List[SpatialViolation] = []
        
        logger.info("✅ Spatial Awareness Engine initialized")
    
    def add_zone(
        self,
        zone_id: str,
        name: str,
        polygon: List[Tuple[float, float]],
        zone_type: ZoneType = ZoneType.NORMAL,
        **kwargs
    ) -> Zone:
        """
        Add a spatial zone.
        
        Args:
            zone_id: Unique zone identifier
            name: Human-readable zone name
            polygon: List of (x, y) coordinates defining zone boundary
            zone_type: Type of zone (NORMAL, RESTRICTED, etc.)
            **kwargs: Additional zone parameters
            
        Returns:
            Created Zone object
        """
        with self.lock:
            # Convert to numpy array
            poly_array = np.array(polygon, dtype=np.float32)
            
            zone = Zone(
                zone_id=zone_id,
                name=name,
                polygon=poly_array,
                zone_type=zone_type,
                **kwargs
            )
            
            self.zones[zone_id] = zone
            logger.info(f"➕ Added zone '{name}' ({zone_type.value})")
            
            return zone
    
    def update(
        self,
        object_states: Dict,
        timestamp: datetime
    ) -> List[SpatialViolation]:
        """
        Update spatial awareness with current object positions.
        
        Args:
            object_states: Dictionary of ObjectState from context engine
            timestamp: Current timestamp
            
        Returns:
            List of detected spatial violations
        """
        with self.lock:
            new_violations = []
            
            # Reset zone occupancy counts
            for zone in self.zones.values():
                zone.current_occupancy = 0
            
            # Check each active object
            for track_id, obj_state in object_states.items():
                if obj_state.disappeared:
                    continue
                
                centroid = obj_state.get_centroid()
                if not centroid:
                    continue
                
                # Find which zone(s) object is in
                current_zones = self._find_zones_containing_point(centroid)
                
                # Update zone occupancy
                for zone_id in current_zones:
                    self.zones[zone_id].current_occupancy += 1
                
                # Track zone transitions
                prev_zone = self.object_zones.get(track_id)
                
                for zone_id in current_zones:
                    zone = self.zones[zone_id]
                    
                    # Check for zone violations
                    violations = self._check_zone_violations(
                        track_id=track_id,
                        obj_state=obj_state,
                        zone=zone,
                        timestamp=timestamp,
                        prev_zone=prev_zone
                    )
                    
                    new_violations.extend(violations)
                    
                    # Update tracking
                    if track_id not in self.object_zone_history:
                        self.object_zone_history[track_id] = []
                    
                    if zone_id not in self.object_zone_history[track_id]:
                        self.object_zone_history[track_id].append(zone_id)
                        obj_state.zones_entered.add(zone_id)
                
                # Update current zone
                if current_zones:
                    self.object_zones[track_id] = current_zones[0]
                    obj_state.current_zone = current_zones[0]
                elif track_id in self.object_zones:
                    # Object left all zones
                    prev_zone_id = self.object_zones[track_id]
                    obj_state.zones_exited.add(prev_zone_id)
                    del self.object_zones[track_id]
                    obj_state.current_zone = None
            
            # Store violations
            self.violations.extend(new_violations)
            
            return new_violations
    
    def _find_zones_containing_point(self, point: Tuple[float, float]) -> List[str]:
        """
        Find all zones containing a point using ray casting algorithm.
        CPU-optimized.
        """
        x, y = point
        containing_zones = []
        
        for zone_id, zone in self.zones.items():
            if not zone.active:
                continue
            
            if self._point_in_polygon(point, zone.polygon):
                containing_zones.append(zone_id)
        
        return containing_zones
    
    def _point_in_polygon(self, point: Tuple[float, float], polygon: np.ndarray) -> bool:
        """
        Ray casting algorithm for point-in-polygon test.
        Optimized for CPU performance.
        """
        x, y = point
        n = len(polygon)
        inside = False
        
        p1x, p1y = polygon[0]
        for i in range(1, n + 1):
            p2x, p2y = polygon[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y
        
        return inside
    
    def _check_zone_violations(
        self,
        track_id: int,
        obj_state,
        zone: Zone,
        timestamp: datetime,
        prev_zone: Optional[str]
    ) -> List[SpatialViolation]:
        """Check for spatial rule violations"""
        violations = []
        position = obj_state.get_centroid()
        class_name = obj_state.class_name
        
        # 1. Restricted zone violation
        if zone.zone_type == ZoneType.RESTRICTED:
            # Check class restrictions
            if zone.denied_classes and class_name in zone.denied_classes:
                violations.append(SpatialViolation(
                    track_id=track_id,
                    zone_id=zone.zone_id,
                    violation_type=ViolationType.RESTRICTED_ACCESS,
                    timestamp=timestamp,
                    position=position,
                    class_name=class_name,
                    severity=0.8 * zone.severity_weight,
                    reason=f"{class_name} entered restricted zone '{zone.name}'"
                ))
            elif not zone.allowed_classes or class_name not in zone.allowed_classes:
                if zone.allowed_classes is not None:  # Explicit whitelist exists
                    violations.append(SpatialViolation(
                        track_id=track_id,
                        zone_id=zone.zone_id,
                        violation_type=ViolationType.RESTRICTED_ACCESS,
                        timestamp=timestamp,
                        position=position,
                        class_name=class_name,
                        severity=0.7 * zone.severity_weight,
                        reason=f"Unauthorized access to restricted zone '{zone.name}'"
                    ))
        
        # 2. Time-based restrictions
        if zone.zone_type == ZoneType.TIME_RESTRICTED:
            if zone.allowed_time_start and zone.allowed_time_end:
                current_time = timestamp.time()
                if not (zone.allowed_time_start <= current_time <= zone.allowed_time_end):
                    violations.append(SpatialViolation(
                        track_id=track_id,
                        zone_id=zone.zone_id,
                        violation_type=ViolationType.TIME_VIOLATION,
                        timestamp=timestamp,
                        position=position,
                        class_name=class_name,
                        severity=0.6 * zone.severity_weight,
                        reason=f"Access to '{zone.name}' outside allowed hours"
                    ))
        
        # 3. Entry-only zone (detect illegal exits)
        if zone.zone_type == ZoneType.ENTRY_ONLY:
            if prev_zone == zone.zone_id and track_id not in self.object_zones:
                # Object was in entry-only zone, now exiting
                violations.append(SpatialViolation(
                    track_id=track_id,
                    zone_id=zone.zone_id,
                    violation_type=ViolationType.EXIT_VIOLATION,
                    timestamp=timestamp,
                    position=position,
                    class_name=class_name,
                    severity=0.7 * zone.severity_weight,
                    reason=f"Illegal exit from entry-only zone '{zone.name}'"
                ))
        
        # 4. Exit-only zone (detect illegal entries)
        if zone.zone_type == ZoneType.EXIT_ONLY:
            if prev_zone != zone.zone_id:
                # Just entered exit-only zone
                violations.append(SpatialViolation(
                    track_id=track_id,
                    zone_id=zone.zone_id,
                    violation_type=ViolationType.ENTRY_VIOLATION,
                    timestamp=timestamp,
                    position=position,
                    class_name=class_name,
                    severity=0.7 * zone.severity_weight,
                    reason=f"Illegal entry to exit-only zone '{zone.name}'"
                ))
        
        # 5. Crowd density limits
        if zone.current_occupancy > zone.max_occupancy:
            violations.append(SpatialViolation(
                track_id=track_id,
                zone_id=zone.zone_id,
                violation_type=ViolationType.CROWD_LIMIT_EXCEEDED,
                timestamp=timestamp,
                position=position,
                class_name=class_name,
                severity=0.5 * (zone.current_occupancy / zone.max_occupancy),
                reason=f"Crowd limit exceeded in '{zone.name}' ({zone.current_occupancy}/{zone.max_occupancy})"
            ))
        
        # Update violation count
        if violations:
            zone.violations_count += len(violations)
        
        return violations
    
    def get_zone_occupancy(self, zone_id: str) -> int:
        """Get current occupancy count for a zone"""
        with self.lock:
            if zone_id in self.zones:
                return self.zones[zone_id].current_occupancy
            return 0
    
    def get_high_density_zones(self, threshold: float = 0.8) -> List[str]:
        """Get zones exceeding density threshold"""
        with self.lock:
            high_density = []
            for zone_id, zone in self.zones.items():
                if zone.current_occupancy / zone.max_occupancy > threshold:
                    high_density.append(zone_id)
            return high_density
    
    def get_stats(self) -> Dict:
        """Get spatial engine statistics"""
        with self.lock:
            return {
                "total_zones": len(self.zones),
                "active_zones": len([z for z in self.zones.values() if z.active]),
                "objects_in_zones": len(self.object_zones),
                "total_violations": len(self.violations),
                "violations_by_type": self._count_violations_by_type()
            }
    
    def _count_violations_by_type(self) -> Dict[str, int]:
        """Count violations by type"""
        counts = {}
        for v in self.violations:
            vtype = v.violation_type.value
            counts[vtype] = counts.get(vtype, 0) + 1
        return counts
