; ModuleID = 'benchmarks\test\PG005_conv2d.c'
source_filename = "benchmarks\\test\\PG005_conv2d.c"
target datalayout = "e-m:w-p270:32:32-p271:32:32-p272:64:64-i64:64-i128:128-f80:128-n8:16:32:64-S128"
target triple = "x86_64-w64-windows-gnu"

@__const.main.k = private unnamed_addr constant [3 x [3 x i32]] [[3 x i32] [i32 1, i32 1, i32 1], [3 x i32] [i32 1, i32 2, i32 1], [3 x i32] [i32 1, i32 1, i32 1]], align 16

; Function Attrs: noinline nounwind uwtable
define dso_local void @conv2d(ptr noundef %0, ptr noundef %1, ptr noundef %2) #0 {
  %4 = alloca ptr, align 8
  %5 = alloca ptr, align 8
  %6 = alloca ptr, align 8
  %7 = alloca i32, align 4
  %8 = alloca i32, align 4
  %9 = alloca i32, align 4
  %10 = alloca i32, align 4
  %11 = alloca i32, align 4
  store ptr %0, ptr %4, align 8
  store ptr %1, ptr %5, align 8
  store ptr %2, ptr %6, align 8
  store i32 1, ptr %7, align 4
  br label %12

12:                                               ; preds = %74, %3
  %13 = load i32, ptr %7, align 4
  %14 = icmp slt i32 %13, 9
  br i1 %14, label %15, label %77

15:                                               ; preds = %12
  store i32 1, ptr %8, align 4
  br label %16

16:                                               ; preds = %70, %15
  %17 = load i32, ptr %8, align 4
  %18 = icmp slt i32 %17, 9
  br i1 %18, label %19, label %73

19:                                               ; preds = %16
  store i32 0, ptr %9, align 4
  store i32 -1, ptr %10, align 4
  br label %20

20:                                               ; preds = %57, %19
  %21 = load i32, ptr %10, align 4
  %22 = icmp sle i32 %21, 1
  br i1 %22, label %23, label %60

23:                                               ; preds = %20
  store i32 -1, ptr %11, align 4
  br label %24

24:                                               ; preds = %53, %23
  %25 = load i32, ptr %11, align 4
  %26 = icmp sle i32 %25, 1
  br i1 %26, label %27, label %56

27:                                               ; preds = %24
  %28 = load ptr, ptr %4, align 8
  %29 = load i32, ptr %7, align 4
  %30 = load i32, ptr %10, align 4
  %31 = add nsw i32 %29, %30
  %32 = sext i32 %31 to i64
  %33 = getelementptr inbounds [10 x i32], ptr %28, i64 %32
  %34 = load i32, ptr %8, align 4
  %35 = load i32, ptr %11, align 4
  %36 = add nsw i32 %34, %35
  %37 = sext i32 %36 to i64
  %38 = getelementptr inbounds [10 x i32], ptr %33, i64 0, i64 %37
  %39 = load i32, ptr %38, align 4
  %40 = load ptr, ptr %6, align 8
  %41 = load i32, ptr %10, align 4
  %42 = add nsw i32 %41, 1
  %43 = sext i32 %42 to i64
  %44 = getelementptr inbounds [3 x i32], ptr %40, i64 %43
  %45 = load i32, ptr %11, align 4
  %46 = add nsw i32 %45, 1
  %47 = sext i32 %46 to i64
  %48 = getelementptr inbounds [3 x i32], ptr %44, i64 0, i64 %47
  %49 = load i32, ptr %48, align 4
  %50 = mul nsw i32 %39, %49
  %51 = load i32, ptr %9, align 4
  %52 = add nsw i32 %51, %50
  store i32 %52, ptr %9, align 4
  br label %53

53:                                               ; preds = %27
  %54 = load i32, ptr %11, align 4
  %55 = add nsw i32 %54, 1
  store i32 %55, ptr %11, align 4
  br label %24, !llvm.loop !7

56:                                               ; preds = %24
  br label %57

57:                                               ; preds = %56
  %58 = load i32, ptr %10, align 4
  %59 = add nsw i32 %58, 1
  store i32 %59, ptr %10, align 4
  br label %20, !llvm.loop !9

60:                                               ; preds = %20
  %61 = load i32, ptr %9, align 4
  %62 = sdiv i32 %61, 9
  %63 = load ptr, ptr %5, align 8
  %64 = load i32, ptr %7, align 4
  %65 = sext i32 %64 to i64
  %66 = getelementptr inbounds [10 x i32], ptr %63, i64 %65
  %67 = load i32, ptr %8, align 4
  %68 = sext i32 %67 to i64
  %69 = getelementptr inbounds [10 x i32], ptr %66, i64 0, i64 %68
  store i32 %62, ptr %69, align 4
  br label %70

70:                                               ; preds = %60
  %71 = load i32, ptr %8, align 4
  %72 = add nsw i32 %71, 1
  store i32 %72, ptr %8, align 4
  br label %16, !llvm.loop !10

73:                                               ; preds = %16
  br label %74

74:                                               ; preds = %73
  %75 = load i32, ptr %7, align 4
  %76 = add nsw i32 %75, 1
  store i32 %76, ptr %7, align 4
  br label %12, !llvm.loop !11

77:                                               ; preds = %12
  ret void
}

; Function Attrs: noinline nounwind uwtable
define dso_local i32 @main() #0 {
  %1 = alloca i32, align 4
  %2 = alloca [10 x [10 x i32]], align 16
  %3 = alloca [10 x [10 x i32]], align 16
  %4 = alloca [3 x [3 x i32]], align 16
  %5 = alloca i32, align 4
  %6 = alloca i32, align 4
  store i32 0, ptr %1, align 4
  call void @llvm.memset.p0.i64(ptr align 16 %3, i8 0, i64 400, i1 false)
  call void @llvm.memcpy.p0.p0.i64(ptr align 16 %4, ptr align 16 @__const.main.k, i64 36, i1 false)
  store i32 0, ptr %5, align 4
  br label %7

7:                                                ; preds = %30, %0
  %8 = load i32, ptr %5, align 4
  %9 = icmp slt i32 %8, 10
  br i1 %9, label %10, label %33

10:                                               ; preds = %7
  store i32 0, ptr %6, align 4
  br label %11

11:                                               ; preds = %26, %10
  %12 = load i32, ptr %6, align 4
  %13 = icmp slt i32 %12, 10
  br i1 %13, label %14, label %29

14:                                               ; preds = %11
  %15 = load i32, ptr %5, align 4
  %16 = mul nsw i32 %15, 3
  %17 = load i32, ptr %6, align 4
  %18 = add nsw i32 %16, %17
  %19 = srem i32 %18, 256
  %20 = load i32, ptr %5, align 4
  %21 = sext i32 %20 to i64
  %22 = getelementptr inbounds [10 x [10 x i32]], ptr %2, i64 0, i64 %21
  %23 = load i32, ptr %6, align 4
  %24 = sext i32 %23 to i64
  %25 = getelementptr inbounds [10 x i32], ptr %22, i64 0, i64 %24
  store i32 %19, ptr %25, align 4
  br label %26

26:                                               ; preds = %14
  %27 = load i32, ptr %6, align 4
  %28 = add nsw i32 %27, 1
  store i32 %28, ptr %6, align 4
  br label %11, !llvm.loop !12

29:                                               ; preds = %11
  br label %30

30:                                               ; preds = %29
  %31 = load i32, ptr %5, align 4
  %32 = add nsw i32 %31, 1
  store i32 %32, ptr %5, align 4
  br label %7, !llvm.loop !13

33:                                               ; preds = %7
  %34 = getelementptr inbounds [10 x [10 x i32]], ptr %2, i64 0, i64 0
  %35 = getelementptr inbounds [10 x [10 x i32]], ptr %3, i64 0, i64 0
  %36 = getelementptr inbounds [3 x [3 x i32]], ptr %4, i64 0, i64 0
  call void @conv2d(ptr noundef %34, ptr noundef %35, ptr noundef %36)
  %37 = getelementptr inbounds [10 x [10 x i32]], ptr %3, i64 0, i64 5
  %38 = getelementptr inbounds [10 x i32], ptr %37, i64 0, i64 5
  %39 = load i32, ptr %38, align 4
  %40 = and i32 %39, 255
  ret i32 %40
}

; Function Attrs: nocallback nofree nosync nounwind willreturn memory(argmem: write)
declare void @llvm.memset.p0.i64(ptr writeonly captures(none), i8, i64, i1 immarg) #1

; Function Attrs: nocallback nofree nosync nounwind willreturn memory(argmem: readwrite)
declare void @llvm.memcpy.p0.p0.i64(ptr noalias writeonly captures(none), ptr noalias readonly captures(none), i64, i1 immarg) #2

attributes #0 = { noinline nounwind uwtable "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #1 = { nocallback nofree nosync nounwind willreturn memory(argmem: write) }
attributes #2 = { nocallback nofree nosync nounwind willreturn memory(argmem: readwrite) }

!llvm.dbg.cu = !{!0}
!llvm.module.flags = !{!2, !3, !4, !5}
!llvm.ident = !{!6}

!0 = distinct !DICompileUnit(language: DW_LANG_C11, file: !1, producer: "clang version 23.1.2 (https://github.com/llvm/llvm-project 85ac560262434c9ccfc0c183ec22d4138ed647fb)", isOptimized: false, runtimeVersion: 0, emissionKind: NoDebug, splitDebugInlining: false, nameTableKind: None)
!1 = !DIFile(filename: "benchmarks\\test\\PG005_conv2d.c", directory: "C:\\COMPILER PROJECT\\llvm-ml-pass-project")
!2 = !{i32 2, !"Debug Info Version", i32 3}
!3 = !{i32 8, !"PIC Level", i32 2}
!4 = !{i32 7, !"uwtable", i32 2}
!5 = !{i32 1, !"MaxTLSAlign", i32 65536}
!6 = !{!"clang version 23.1.2 (https://github.com/llvm/llvm-project 85ac560262434c9ccfc0c183ec22d4138ed647fb)"}
!7 = distinct !{!7, !8}
!8 = !{!"llvm.loop.mustprogress"}
!9 = distinct !{!9, !8}
!10 = distinct !{!10, !8}
!11 = distinct !{!11, !8}
!12 = distinct !{!12, !8}
!13 = distinct !{!13, !8}
