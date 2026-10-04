; ModuleID = 'benchmarks/val/PG030_ring_buffer.c'
source_filename = "benchmarks/val/PG030_ring_buffer.c"
target datalayout = "e-m:w-p270:32:32-p271:32:32-p272:64:64-i64:64-i128:128-f80:128-n8:16:32:64-S128"
target triple = "x86_64-w64-windows-gnu"

%struct.RingBuffer = type { [8 x i32], i32, i32, i32 }

; Function Attrs: noinline nounwind uwtable
define dso_local void @rb_init(ptr noundef %0) #0 {
  %2 = alloca ptr, align 8
  store ptr %0, ptr %2, align 8
  %3 = load ptr, ptr %2, align 8
  %4 = getelementptr inbounds nuw %struct.RingBuffer, ptr %3, i32 0, i32 1
  store i32 0, ptr %4, align 4
  %5 = load ptr, ptr %2, align 8
  %6 = getelementptr inbounds nuw %struct.RingBuffer, ptr %5, i32 0, i32 2
  store i32 0, ptr %6, align 4
  %7 = load ptr, ptr %2, align 8
  %8 = getelementptr inbounds nuw %struct.RingBuffer, ptr %7, i32 0, i32 3
  store i32 0, ptr %8, align 4
  ret void
}

; Function Attrs: noinline nounwind uwtable
define dso_local i32 @rb_push(ptr noundef %0, i32 noundef %1) #0 {
  %3 = alloca i32, align 4
  %4 = alloca ptr, align 8
  %5 = alloca i32, align 4
  store ptr %0, ptr %4, align 8
  store i32 %1, ptr %5, align 4
  %6 = load ptr, ptr %4, align 8
  %7 = getelementptr inbounds nuw %struct.RingBuffer, ptr %6, i32 0, i32 3
  %8 = load i32, ptr %7, align 4
  %9 = icmp eq i32 %8, 8
  br i1 %9, label %10, label %11

10:                                               ; preds = %2
  store i32 0, ptr %3, align 4
  br label %31

11:                                               ; preds = %2
  %12 = load i32, ptr %5, align 4
  %13 = load ptr, ptr %4, align 8
  %14 = getelementptr inbounds nuw %struct.RingBuffer, ptr %13, i32 0, i32 0
  %15 = load ptr, ptr %4, align 8
  %16 = getelementptr inbounds nuw %struct.RingBuffer, ptr %15, i32 0, i32 2
  %17 = load i32, ptr %16, align 4
  %18 = sext i32 %17 to i64
  %19 = getelementptr inbounds [8 x i32], ptr %14, i64 0, i64 %18
  store i32 %12, ptr %19, align 4
  %20 = load ptr, ptr %4, align 8
  %21 = getelementptr inbounds nuw %struct.RingBuffer, ptr %20, i32 0, i32 2
  %22 = load i32, ptr %21, align 4
  %23 = add nsw i32 %22, 1
  %24 = srem i32 %23, 8
  %25 = load ptr, ptr %4, align 8
  %26 = getelementptr inbounds nuw %struct.RingBuffer, ptr %25, i32 0, i32 2
  store i32 %24, ptr %26, align 4
  %27 = load ptr, ptr %4, align 8
  %28 = getelementptr inbounds nuw %struct.RingBuffer, ptr %27, i32 0, i32 3
  %29 = load i32, ptr %28, align 4
  %30 = add nsw i32 %29, 1
  store i32 %30, ptr %28, align 4
  store i32 1, ptr %3, align 4
  br label %31

31:                                               ; preds = %11, %10
  %32 = load i32, ptr %3, align 4
  ret i32 %32
}

; Function Attrs: noinline nounwind uwtable
define dso_local i32 @rb_pop(ptr noundef %0, ptr noundef %1) #0 {
  %3 = alloca i32, align 4
  %4 = alloca ptr, align 8
  %5 = alloca ptr, align 8
  store ptr %0, ptr %4, align 8
  store ptr %1, ptr %5, align 8
  %6 = load ptr, ptr %4, align 8
  %7 = getelementptr inbounds nuw %struct.RingBuffer, ptr %6, i32 0, i32 3
  %8 = load i32, ptr %7, align 4
  %9 = icmp eq i32 %8, 0
  br i1 %9, label %10, label %11

10:                                               ; preds = %2
  store i32 0, ptr %3, align 4
  br label %32

11:                                               ; preds = %2
  %12 = load ptr, ptr %4, align 8
  %13 = getelementptr inbounds nuw %struct.RingBuffer, ptr %12, i32 0, i32 0
  %14 = load ptr, ptr %4, align 8
  %15 = getelementptr inbounds nuw %struct.RingBuffer, ptr %14, i32 0, i32 1
  %16 = load i32, ptr %15, align 4
  %17 = sext i32 %16 to i64
  %18 = getelementptr inbounds [8 x i32], ptr %13, i64 0, i64 %17
  %19 = load i32, ptr %18, align 4
  %20 = load ptr, ptr %5, align 8
  store i32 %19, ptr %20, align 4
  %21 = load ptr, ptr %4, align 8
  %22 = getelementptr inbounds nuw %struct.RingBuffer, ptr %21, i32 0, i32 1
  %23 = load i32, ptr %22, align 4
  %24 = add nsw i32 %23, 1
  %25 = srem i32 %24, 8
  %26 = load ptr, ptr %4, align 8
  %27 = getelementptr inbounds nuw %struct.RingBuffer, ptr %26, i32 0, i32 1
  store i32 %25, ptr %27, align 4
  %28 = load ptr, ptr %4, align 8
  %29 = getelementptr inbounds nuw %struct.RingBuffer, ptr %28, i32 0, i32 3
  %30 = load i32, ptr %29, align 4
  %31 = add nsw i32 %30, -1
  store i32 %31, ptr %29, align 4
  store i32 1, ptr %3, align 4
  br label %32

32:                                               ; preds = %11, %10
  %33 = load i32, ptr %3, align 4
  ret i32 %33
}

; Function Attrs: noinline nounwind uwtable
define dso_local i32 @main() #0 {
  %1 = alloca i32, align 4
  %2 = alloca %struct.RingBuffer, align 4
  %3 = alloca i32, align 4
  %4 = alloca i32, align 4
  %5 = alloca i32, align 4
  store i32 0, ptr %1, align 4
  call void @rb_init(ptr noundef %2)
  store i32 0, ptr %3, align 4
  br label %6

6:                                                ; preds = %13, %0
  %7 = load i32, ptr %3, align 4
  %8 = icmp slt i32 %7, 6
  br i1 %8, label %9, label %16

9:                                                ; preds = %6
  %10 = load i32, ptr %3, align 4
  %11 = mul nsw i32 %10, 10
  %12 = call i32 @rb_push(ptr noundef %2, i32 noundef %11)
  br label %13

13:                                               ; preds = %9
  %14 = load i32, ptr %3, align 4
  %15 = add nsw i32 %14, 1
  store i32 %15, ptr %3, align 4
  br label %6, !llvm.loop !7

16:                                               ; preds = %6
  %17 = call i32 @rb_pop(ptr noundef %2, ptr noundef %4)
  %18 = call i32 @rb_pop(ptr noundef %2, ptr noundef %5)
  %19 = load i32, ptr %4, align 4
  %20 = load i32, ptr %5, align 4
  %21 = add nsw i32 %19, %20
  %22 = getelementptr inbounds nuw %struct.RingBuffer, ptr %2, i32 0, i32 3
  %23 = load i32, ptr %22, align 4
  %24 = add nsw i32 %21, %23
  %25 = and i32 %24, 255
  ret i32 %25
}

attributes #0 = { noinline nounwind uwtable "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }

!llvm.dbg.cu = !{!0}
!llvm.module.flags = !{!2, !3, !4, !5}
!llvm.ident = !{!6}

!0 = distinct !DICompileUnit(language: DW_LANG_C11, file: !1, producer: "clang version 23.1.2 (https://github.com/llvm/llvm-project 85ac560262434c9ccfc0c183ec22d4138ed647fb)", isOptimized: false, runtimeVersion: 0, emissionKind: NoDebug, splitDebugInlining: false, nameTableKind: None)
!1 = !DIFile(filename: "benchmarks/val\\PG030_ring_buffer.c", directory: "C:\\COMPILER PROJECT\\llvm-ml-pass-project")
!2 = !{i32 2, !"Debug Info Version", i32 3}
!3 = !{i32 8, !"PIC Level", i32 2}
!4 = !{i32 7, !"uwtable", i32 2}
!5 = !{i32 1, !"MaxTLSAlign", i32 65536}
!6 = !{!"clang version 23.1.2 (https://github.com/llvm/llvm-project 85ac560262434c9ccfc0c183ec22d4138ed647fb)"}
!7 = distinct !{!7, !8}
!8 = !{!"llvm.loop.mustprogress"}
