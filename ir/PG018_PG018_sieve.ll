; ModuleID = 'benchmarks/train/PG018_sieve.c'
source_filename = "benchmarks/train/PG018_sieve.c"
target datalayout = "e-m:w-p270:32:32-p271:32:32-p272:64:64-i64:64-i128:128-f80:128-n8:16:32:64-S128"
target triple = "x86_64-w64-windows-gnu"

; Function Attrs: noinline nounwind uwtable
define dso_local i32 @count_primes(i32 noundef %0) #0 {
  %2 = alloca i32, align 4
  %3 = alloca [100 x i8], align 16
  %4 = alloca i32, align 4
  %5 = alloca i32, align 4
  %6 = alloca i32, align 4
  %7 = alloca i32, align 4
  %8 = alloca i32, align 4
  store i32 %0, ptr %2, align 4
  store i32 0, ptr %4, align 4
  br label %9

9:                                                ; preds = %17, %1
  %10 = load i32, ptr %4, align 4
  %11 = load i32, ptr %2, align 4
  %12 = icmp slt i32 %10, %11
  br i1 %12, label %13, label %20

13:                                               ; preds = %9
  %14 = load i32, ptr %4, align 4
  %15 = sext i32 %14 to i64
  %16 = getelementptr inbounds [100 x i8], ptr %3, i64 0, i64 %15
  store i8 1, ptr %16, align 1
  br label %17

17:                                               ; preds = %13
  %18 = load i32, ptr %4, align 4
  %19 = add nsw i32 %18, 1
  store i32 %19, ptr %4, align 4
  br label %9, !llvm.loop !7

20:                                               ; preds = %9
  %21 = getelementptr inbounds [100 x i8], ptr %3, i64 0, i64 1
  store i8 0, ptr %21, align 1
  %22 = getelementptr inbounds [100 x i8], ptr %3, i64 0, i64 0
  store i8 0, ptr %22, align 16
  store i32 2, ptr %5, align 4
  br label %23

23:                                               ; preds = %53, %20
  %24 = load i32, ptr %5, align 4
  %25 = load i32, ptr %5, align 4
  %26 = mul nsw i32 %24, %25
  %27 = load i32, ptr %2, align 4
  %28 = icmp slt i32 %26, %27
  br i1 %28, label %29, label %56

29:                                               ; preds = %23
  %30 = load i32, ptr %5, align 4
  %31 = sext i32 %30 to i64
  %32 = getelementptr inbounds [100 x i8], ptr %3, i64 0, i64 %31
  %33 = load i8, ptr %32, align 1
  %34 = icmp ne i8 %33, 0
  br i1 %34, label %35, label %52

35:                                               ; preds = %29
  %36 = load i32, ptr %5, align 4
  %37 = load i32, ptr %5, align 4
  %38 = mul nsw i32 %36, %37
  store i32 %38, ptr %6, align 4
  br label %39

39:                                               ; preds = %47, %35
  %40 = load i32, ptr %6, align 4
  %41 = load i32, ptr %2, align 4
  %42 = icmp slt i32 %40, %41
  br i1 %42, label %43, label %51

43:                                               ; preds = %39
  %44 = load i32, ptr %6, align 4
  %45 = sext i32 %44 to i64
  %46 = getelementptr inbounds [100 x i8], ptr %3, i64 0, i64 %45
  store i8 0, ptr %46, align 1
  br label %47

47:                                               ; preds = %43
  %48 = load i32, ptr %5, align 4
  %49 = load i32, ptr %6, align 4
  %50 = add nsw i32 %49, %48
  store i32 %50, ptr %6, align 4
  br label %39, !llvm.loop !9

51:                                               ; preds = %39
  br label %52

52:                                               ; preds = %51, %29
  br label %53

53:                                               ; preds = %52
  %54 = load i32, ptr %5, align 4
  %55 = add nsw i32 %54, 1
  store i32 %55, ptr %5, align 4
  br label %23, !llvm.loop !10

56:                                               ; preds = %23
  store i32 0, ptr %7, align 4
  store i32 2, ptr %8, align 4
  br label %57

57:                                               ; preds = %71, %56
  %58 = load i32, ptr %8, align 4
  %59 = load i32, ptr %2, align 4
  %60 = icmp slt i32 %58, %59
  br i1 %60, label %61, label %74

61:                                               ; preds = %57
  %62 = load i32, ptr %8, align 4
  %63 = sext i32 %62 to i64
  %64 = getelementptr inbounds [100 x i8], ptr %3, i64 0, i64 %63
  %65 = load i8, ptr %64, align 1
  %66 = icmp ne i8 %65, 0
  br i1 %66, label %67, label %70

67:                                               ; preds = %61
  %68 = load i32, ptr %7, align 4
  %69 = add nsw i32 %68, 1
  store i32 %69, ptr %7, align 4
  br label %70

70:                                               ; preds = %67, %61
  br label %71

71:                                               ; preds = %70
  %72 = load i32, ptr %8, align 4
  %73 = add nsw i32 %72, 1
  store i32 %73, ptr %8, align 4
  br label %57, !llvm.loop !11

74:                                               ; preds = %57
  %75 = load i32, ptr %7, align 4
  ret i32 %75
}

; Function Attrs: noinline nounwind uwtable
define dso_local i32 @main() #0 {
  %1 = alloca i32, align 4
  store i32 0, ptr %1, align 4
  %2 = call i32 @count_primes(i32 noundef 100)
  ret i32 %2
}

attributes #0 = { noinline nounwind uwtable "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }

!llvm.dbg.cu = !{!0}
!llvm.module.flags = !{!2, !3, !4, !5}
!llvm.ident = !{!6}

!0 = distinct !DICompileUnit(language: DW_LANG_C11, file: !1, producer: "clang version 23.1.2 (https://github.com/llvm/llvm-project 85ac560262434c9ccfc0c183ec22d4138ed647fb)", isOptimized: false, runtimeVersion: 0, emissionKind: NoDebug, splitDebugInlining: false, nameTableKind: None)
!1 = !DIFile(filename: "benchmarks/train\\PG018_sieve.c", directory: "C:\\COMPILER PROJECT\\llvm-ml-pass-project")
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
