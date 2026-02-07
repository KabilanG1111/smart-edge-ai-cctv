"""
Quick test script for GStreamer camera integration
Tests both USB and frame reading compatibility
"""

import cv2
import time


def test_gstreamer_import():
    """Test if GStreamer module can be imported."""
    print("=" * 60)
    print("TEST 1: Import GStreamer module")
    print("=" * 60)
    
    try:
        from core.camera_gstreamer import GStreamerCamera
        print("✅ GStreamerCamera imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Failed to import: {e}")
        return False


def test_usb_camera():
    """Test USB camera with GStreamer."""
    print("\n" + "=" * 60)
    print("TEST 2: USB Camera with GStreamer")
    print("=" * 60)
    
    try:
        from core.camera_gstreamer import GStreamerCamera
        
        print("Opening USB camera (device 0)...")
        camera = GStreamerCamera(source=0, pipeline_type='usb')
        
        if not camera.isOpened():
            print("❌ Camera failed to open")
            return False
        
        print("✅ Camera opened successfully")
        
        # Read 10 test frames
        print("Reading 10 frames...")
        for i in range(10):
            ret, frame = camera.read()
            if not ret:
                print(f"❌ Failed to read frame {i+1}")
                camera.release()
                return False
            
            print(f"✅ Frame {i+1}: shape={frame.shape}, dtype={frame.dtype}")
            
            # Verify frame is valid BGR numpy array
            if len(frame.shape) != 3 or frame.shape[2] != 3:
                print(f"❌ Invalid frame shape: {frame.shape}")
                camera.release()
                return False
        
        camera.release()
        print("✅ USB camera test PASSED")
        return True
        
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False


def test_api_compatibility():
    """Test that GStreamer camera has same API as cv2.VideoCapture."""
    print("\n" + "=" * 60)
    print("TEST 3: API Compatibility with cv2.VideoCapture")
    print("=" * 60)
    
    try:
        from core.camera_gstreamer import GStreamerCamera
        
        camera = GStreamerCamera(source=0, pipeline_type='usb')
        
        # Check required methods exist
        required_methods = ['read', 'isOpened', 'release']
        for method in required_methods:
            if not hasattr(camera, method):
                print(f"❌ Missing method: {method}")
                return False
            print(f"✅ Method exists: {method}")
        
        # Test method signatures
        ret, frame = camera.read()
        print(f"✅ read() returns: ({type(ret).__name__}, {type(frame).__name__})")
        
        is_opened = camera.isOpened()
        print(f"✅ isOpened() returns: {type(is_opened).__name__}")
        
        camera.release()
        print("✅ release() executed without error")
        
        print("✅ API compatibility test PASSED")
        return True
        
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False


def test_opencv_comparison():
    """Compare GStreamer vs OpenCV frame reading."""
    print("\n" + "=" * 60)
    print("TEST 4: Performance Comparison (OpenCV vs GStreamer)")
    print("=" * 60)
    
    try:
        from core.camera_gstreamer import GStreamerCamera
        
        # Test OpenCV
        print("\nTesting OpenCV VideoCapture...")
        cap_cv = cv2.VideoCapture(0)
        if not cap_cv.isOpened():
            print("❌ OpenCV camera failed to open")
            return False
        
        start = time.time()
        for i in range(30):
            ret, frame = cap_cv.read()
            if not ret:
                break
        opencv_time = time.time() - start
        cap_cv.release()
        
        print(f"✅ OpenCV: {opencv_time:.2f}s for 30 frames ({30/opencv_time:.1f} fps)")
        
        # Test GStreamer
        print("\nTesting GStreamer...")
        cap_gs = GStreamerCamera(source=0, pipeline_type='usb')
        if not cap_gs.isOpened():
            print("❌ GStreamer camera failed to open")
            return False
        
        start = time.time()
        for i in range(30):
            ret, frame = cap_gs.read()
            if not ret:
                break
        gstreamer_time = time.time() - start
        cap_gs.release()
        
        print(f"✅ GStreamer: {gstreamer_time:.2f}s for 30 frames ({30/gstreamer_time:.1f} fps)")
        
        # Compare
        speedup = opencv_time / gstreamer_time
        print(f"\n📊 Performance: GStreamer is {speedup:.2f}x {'faster' if speedup > 1 else 'slower'} than OpenCV")
        
        return True
        
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False


def test_motion_detection_integration():
    """Test that motion detection works with GStreamer frames."""
    print("\n" + "=" * 60)
    print("TEST 5: Motion Detection Integration")
    print("=" * 60)
    
    try:
        from core.camera_gstreamer import GStreamerCamera
        from core.motion_detector import MotionDetector
        
        camera = GStreamerCamera(source=0, pipeline_type='usb')
        detector = MotionDetector()
        
        print("Reading frames and running motion detection...")
        for i in range(10):
            ret, frame = camera.read()
            if not ret:
                print(f"❌ Failed to read frame {i+1}")
                camera.release()
                return False
            
            # Run motion detection
            boxes, thresh = detector.detect(frame)
            print(f"✅ Frame {i+1}: {len(boxes)} motion(s) detected")
        
        camera.release()
        print("✅ Motion detection integration test PASSED")
        return True
        
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False


def main():
    """Run all tests."""
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 10 + "GSTREAMER CAMERA INTEGRATION TEST" + " " * 15 + "║")
    print("╚" + "═" * 58 + "╝")
    
    tests = [
        ("Import Test", test_gstreamer_import),
        ("USB Camera Test", test_usb_camera),
        ("API Compatibility Test", test_api_compatibility),
        ("Performance Comparison", test_opencv_comparison),
        ("Motion Detection Integration", test_motion_detection_integration)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ {test_name} crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print("\n" + "=" * 60)
    print(f"Results: {passed}/{total} tests passed")
    print("=" * 60)
    
    if passed == total:
        print("\n🎉 All tests passed! GStreamer integration is ready.")
    else:
        print("\n⚠ Some tests failed. Check output above for details.")


if __name__ == "__main__":
    main()
