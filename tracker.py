import cv2

def check_opencv_tracking():
    """检查OpenCV跟踪器支持"""
    print(f"OpenCV版本: {cv2.__version__}")
    
    # 检查可用的跟踪器
    tracker_types = ['KCF', 'CSRT', 'MOSSE', 'MedianFlow', 'MIL', 'Boosting']
    available_trackers = []
    
    for tracker_type in tracker_types:
        try:
            if tracker_type == 'KCF':
                tracker = cv2.TrackerKCF_create()
            elif tracker_type == 'CSRT':
                tracker = cv2.TrackerCSRT_create()
            elif tracker_type == 'MOSSE':
                tracker = cv2.TrackerMOSSE_create()
            elif tracker_type == 'MedianFlow':
                tracker = cv2.TrackerMedianFlow_create()
            elif tracker_type == 'MIL':
                tracker = cv2.TrackerMIL_create()
            elif tracker_type == 'Boosting':
                tracker = cv2.TrackerBoosting_create()
            
            # 测试创建是否成功
            if tracker is not None:
                available_trackers.append(tracker_type)
                print(f"✅ {tracker_type} 跟踪器可用")
            else:
                print(f"❌ {tracker_type} 跟踪器创建失败")
                
        except Exception as e:
            print(f"❌ {tracker_type} 跟踪器错误: {e}")
    
    return available_trackers

def robust_tracker_initialization():
    """稳健的跟踪器初始化"""
    source = 0
    cap = cv2.VideoCapture(source)
    
    # 设置摄像头参数
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    # 读取多帧以确保稳定
    for i in range(10):
        ret, frame = cap.read()
        if not ret:
            print(f"❌ 第{i+1}次读取失败")
            continue
    
    if not ret:
        print("❌ 无法读取摄像头")
        return
    
    print("✅ 摄像头读取成功")
    print(f"图像尺寸: {frame.shape}")
    
    # 检查可用的跟踪器
    available_trackers = check_opencv_tracking()
    
    if not available_trackers:
        print("❌ 没有可用的跟踪器，请重新安装OpenCV")
        cap.release()
        return
    
    # 使用推荐的边界框
    height, width = frame.shape[:2]
    bbox = (width//4, height//4, width//2, height//2)
    print(f"使用边界框: {bbox}")
    
    # 显示边界框
    display_frame = frame.copy()
    x, y, w, h = bbox
    cv2.rectangle(display_frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    cv2.imshow('跟踪区域', display_frame)
    cv2.waitKey(1000)
    cv2.destroyAllWindows()
    
    # 按优先级尝试不同的跟踪器
    tracker_priority = ['CSRT', 'KCF', 'MOSSE', 'MedianFlow', 'MIL']
    
    tracker = None
    tracker_name = None
    
    for tracker_type in tracker_priority:
        if tracker_type not in available_trackers:
            continue
            
        try:
            print(f"\n尝试初始化 {tracker_type} 跟踪器...")
            
            if tracker_type == 'KCF':
                tracker = cv2.TrackerKCF_create()
            elif tracker_type == 'CSRT':
                tracker = cv2.TrackerCSRT_create()
            elif tracker_type == 'MOSSE':
                tracker = cv2.TrackerMOSSE_create()
            elif tracker_type == 'MedianFlow':
                tracker = cv2.TrackerMedianFlow_create()
            elif tracker_type == 'MIL':
                tracker = cv2.TrackerMIL_create()
            
            # 使用图像副本进行初始化
            frame_copy = frame.copy()
            success = tracker.init(frame_copy, bbox)
            
            if success:
                # 测试更新
                test_success, test_bbox = tracker.update(frame_copy)
                if test_success:
                    tracker_name = tracker_type
                    print(f"✅ {tracker_type} 跟踪器初始化并测试成功!")
                    break
                else:
                    print(f"⚠️ {tracker_type} 初始化成功但测试更新失败")
            else:
                print(f"❌ {tracker_type} 跟踪器初始化失败")
                
        except Exception as e:
            print(f"❌ {tracker_type} 跟踪器异常: {e}")
    
    if tracker is None:
        print("\n💡 所有跟踪器都失败，建议:")
        print("1. 重新安装 OpenCV: pip install opencv-contrib-python")
        print("2. 检查摄像头权限")
        print("3. 尝试其他摄像头源")
        cap.release()
        return
    
    print(f"\n🎉 使用 {tracker_name} 跟踪器开始跟踪...")
    print("按 'q' 退出跟踪")
    
    # 跟踪循环
    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ 无法读取帧")
            break
        
        success, bbox = tracker.update(frame)
        
        if success:
            x, y, w, h = [int(i) for i in bbox]
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, f"{tracker_name} Tracking", (x, y-10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        else:
            cv2.putText(frame, "Tracking Lost", (50, 50), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
        cv2.imshow("Tracking", frame)
        
        # 退出条件
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('r'):  # 按 'r' 重新初始化
            print("重新初始化跟踪器...")
            bbox = cv2.selectROI("重新选择目标", frame, False)
            if bbox != (0, 0, 0, 0):
                tracker = cv2.TrackerCSRT_create()
                success = tracker.init(frame, bbox)
                if success:
                    print("✅ 重新初始化成功")
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    robust_tracker_initialization()