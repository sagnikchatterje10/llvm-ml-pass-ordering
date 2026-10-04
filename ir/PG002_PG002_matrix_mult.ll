; ModuleID = 'benchmarks/train/PG002_matrix_mult.c'
source_filename = "benchmarks/train/PG002_matrix_mult.c"
target datalayout = "e-m:w-p270:32:32-p271:32:32-p272:64:64-i64:64-i128:128-f80:128-n8:16:32:64-S128"
target triple = "x86_64-w64-windows-gnu"

; Function Attrs: noinline nounwind uwtable
define dso_local void @matmul(ptr noundef %0, ptr noundef %1, ptr noundef %2) #0 {
  %4 = alloca ptr, align 8
  %5 = alloca ptr, align 8
  %6 = alloca ptr, align 8
  %7 = alloca i32, align 4
  %8 = alloca i32, align 4
  %9 = alloca i32, align 4
  %10 = alloca i32, align 4
  store ptr %0, ptr %4, align 8
  store ptr %1, ptr %5, align 8
  store ptr %2, ptr %6, align 8
  store i32 0, ptr %7, align 4
  br label %11

11:                                               ; preds = %58, %3
  %12 = load i32, ptr %7, align 4
  %13 = icmp slt i32 %12, 8
  br i1 %13, label %14, label %61

14:                                               ; preds = %11
  store i32 0, ptr %8, align 4
  br label %15

15:                                               ; preds = %54, %14
  %16 = load i32, ptr %8, align 4
  %17 = icmp slt i32 %16, 8
  br i1 %17, label %18, label %57

18:                                               ; preds = %15
  store i32 0, ptr %9, align 4
  store i32 0, ptr %10, align 4
  br label %19

19:                                               ; preds = %42, %18
  %20 = load i32, ptr %10, align 4
  %21 = icmp slt i32 %20, 8
  br i1 %21, label %22, label %45

22:                                               ; preds = %19
  %23 = load ptr, ptr %4, align 8
  %24 = load i32, ptr %7, align 4
  %25 = sext i32 %24 to i64
  %26 = getelementptr inbounds [8 x i32], ptr %23, i64 %25
  %27 = load i32, ptr %10, align 4
  %28 = sext i32 %27 to i64
  %29 = getelementptr inbounds [8 x i32], ptr %26, i64 0, i64 %28
  %30 = load i32, ptr %29, align 4
  %31 = load ptr, ptr %5, align 8
  %32 = load i32, ptr %10, align 4
  %33 = sext i32 %32 to i64
  %34 = getelementptr inbounds [8 x i32], ptr %31, i64 %33
  %35 = load i32, ptr %8, align 4
  %36 = sext i32 %35 to i64
  %37 = getelementptr inbounds [8 x i32], ptr %34, i64 0, i64 %36
  %38 = load i32, ptr %37, align 4
  %39 = mul nsw i32 %30, %38
  %40 = load i32, ptr %9, align 4
  %41 = add nsw i32 %40, %39
  store i32 %41, ptr %9, align 4
  br label %42

42:                                               ; preds = %22
  %43 = load i32, ptr %10, align 4
  %44 = add nsw i32 %43, 1
  store i32 %44, ptr %10, align 4
  br label %19, !llvm.loop !7

45:                                               ; preds = %19
  %46 = load i32, ptr %9, align 4
  %47 = load ptr, ptr %6, align 8
  %48 = load i32, ptr %7, align 4
  %49 = sext i32 %48 to i64
  %50 = getelementptr inbounds [8 x i32], ptr %47, i64 %49
  %51 = load i32, ptr %8, align 4
  %52 = sext i32 %51 to i64
  %53 = getelementptr inbounds [8 x i32], ptr %50, i64 0, i64 %52
  store i32 %46, ptr %53, align 4
  br label %54

54:                                               ; preds = %45
  %55 = load i32, ptr %8, align 4
  %56 = add nsw i32 %55, 1
  store i32 %56, ptr %8, align 4
  br label %15, !llvm.loop !9

57:                                               ; preds = %15
  br label %58

58:                                               ; preds = %57
  %59 = load i32, ptr %7, align 4
  %60 = add nsw i32 %59, 1
  store i32 %60, ptr %7, align 4
  br label %11, !llvm.loop !10

61:                                               ; preds = %11
  ret void
}

; Function Attrs: noinline nounwind uwtable
define dso_local i32 @main() #0 {
  %1 = alloca i32, align 4
  %2 = alloca [8 x [8 x i32]], align 16
  %3 = alloca [8 x [8 x i32]], align 16
  %4 = alloca [8 x [8 x i32]], align 16
  %5 = alloca i32, align 4
  %6 = alloca i32, align 4
  store i32 0, ptr %1, align 4
  store i32 0, ptr %5, align 4
  br label %7

7:                                                ; preds = %46, %0
  %8 = load i32, ptr %5, align 4
  %9 = icmp slt i32 %8, 8
  br i1 %9, label %10, label %49

10:                                               ; preds = %7
  store i32 0, ptr %6, align 4
  br label %11

11:                                               ; preds = %42, %10
  %12 = load i32, ptr %6, align 4
  %13 = icmp slt i32 %12, 8
  br i1 %13, label %14, label %45

14:                                               ; preds = %11
  %15 = load i32, ptr %5, align 4
  %16 = load i32, ptr %6, align 4
  %17 = add nsw i32 %15, %16
  %18 = and i32 %17, 7
  %19 = load i32, ptr %5, align 4
  %20 = sext i32 %19 to i64
  %21 = getelementptr inbounds [8 x [8 x i32]], ptr %2, i64 0, i64 %20
  %22 = load i32, ptr %6, align 4
  %23 = sext i32 %22 to i64
  %24 = getelementptr inbounds [8 x i32], ptr %21, i64 0, i64 %23
  store i32 %18, ptr %24, align 4
  %25 = load i32, ptr %5, align 4
  %26 = load i32, ptr %6, align 4
  %27 = mul nsw i32 %25, %26
  %28 = add nsw i32 %27, 1
  %29 = and i32 %28, 7
  %30 = load i32, ptr %5, align 4
  %31 = sext i32 %30 to i64
  %32 = getelementptr inbounds [8 x [8 x i32]], ptr %3, i64 0, i64 %31
  %33 = load i32, ptr %6, align 4
  %34 = sext i32 %33 to i64
  %35 = getelementptr inbounds [8 x i32], ptr %32, i64 0, i64 %34
  store i32 %29, ptr %35, align 4
  %36 = load i32, ptr %5, align 4
  %37 = sext i32 %36 to i64
  %38 = getelementptr inbounds [8 x [8 x i32]], ptr %4, i64 0, i64 %37
  %39 = load i32, ptr %6, align 4
  %40 = sext i32 %39 to i64
  %41 = getelementptr inbounds [8 x i32], ptr %38, i64 0, i64 %40
  store i32 0, ptr %41, align 4
  br label %42

42:                                               ; preds = %14
  %43 = load i32, ptr %6, align 4
  %44 = add nsw i32 %43, 1
  store i32 %44, ptr %6, align 4
  br label %11, !llvm.loop !11

45:                                               ; preds = %11
  br label %46

46:                                               ; preds = %45
  %47 = load i32, ptr %5, align 4
  %48 = add nsw i32 %47, 1
  store i32 %48, ptr %5, align 4
  br label %7, !llvm.loop !12

49:                                               ; preds = %7
  %50 = getelementptr inbounds [8 x [8 x i32]], ptr %2, i64 0, i64 0
  %51 = getelementptr inbounds [8 x [8 x i32]], ptr %3, i64 0, i64 0
  %52 = getelementptr inbounds [8 x [8 x i32]], ptr %4, i64 0, i64 0
  call void @matmul(ptr noundef %50, ptr noundef %51, ptr noundef %52)
  %53 = getelementptr inbounds [8 x [8 x i32]], ptr %4, i64 0, i64 0
  %54 = getelementptr inbounds [8 x i32], ptr %53, i64 0, i64 0
  %55 = load i32, ptr %54, align 16
  %56 = getelementptr inbounds [8 x [8 x i32]], ptr %4, i64 0, i64 7
  %57 = getelementptr inbounds [8 x i32], ptr %56, i64 0, i64 7
  %58 = load i32, ptr %57, align 4
  %59 = add nsw i32 %55, %58
  ret i32 %59
}

attributes #0 = { noinline nounwind uwtable "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }

!llvm.dbg.cu = !{!0}
!llvm.module.flags = !{!2, !3, !4, !5}
!llvm.ident = !{!6}

!0 = distinct !DICompileUnit(language: DW_LANG_C11, file: !1, producer: "clang version 23.1.2 (https://github.com/llvm/llvm-project 85ac560262434c9ccfc0c183ec22d4138ed647fb)", isOptimized: false, runtimeVersion: 0, emissionKind: NoDebug, splitDebugInlining: false, nameTableKind: None)
!1 = !DIFile(filename: "benchmarks/train\\PG002_matrix_mult.c", directory: "C:\\COMPILER PROJECT\\llvm-ml-pass-project")
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
