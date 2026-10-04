; ModuleID = 'benchmarks\test\PG020_horner_eval.c'
source_filename = "benchmarks\\test\\PG020_horner_eval.c"
target datalayout = "e-m:w-p270:32:32-p271:32:32-p272:64:64-i64:64-i128:128-f80:128-n8:16:32:64-S128"
target triple = "x86_64-w64-windows-gnu"

; Function Attrs: noinline nounwind uwtable
define dso_local double @horner(ptr noundef %0, i32 noundef %1, double noundef %2) #0 {
  %4 = alloca ptr, align 8
  %5 = alloca i32, align 4
  %6 = alloca double, align 8
  %7 = alloca double, align 8
  %8 = alloca i32, align 4
  store ptr %0, ptr %4, align 8
  store i32 %1, ptr %5, align 4
  store double %2, ptr %6, align 8
  %9 = load ptr, ptr %4, align 8
  %10 = getelementptr inbounds double, ptr %9, i64 0
  %11 = load double, ptr %10, align 8
  store double %11, ptr %7, align 8
  store i32 1, ptr %8, align 4
  br label %12

12:                                               ; preds = %25, %3
  %13 = load i32, ptr %8, align 4
  %14 = load i32, ptr %5, align 4
  %15 = icmp sle i32 %13, %14
  br i1 %15, label %16, label %28

16:                                               ; preds = %12
  %17 = load double, ptr %7, align 8
  %18 = load double, ptr %6, align 8
  %19 = load ptr, ptr %4, align 8
  %20 = load i32, ptr %8, align 4
  %21 = sext i32 %20 to i64
  %22 = getelementptr inbounds double, ptr %19, i64 %21
  %23 = load double, ptr %22, align 8
  %24 = call double @llvm.fmuladd.f64(double %17, double %18, double %23)
  store double %24, ptr %7, align 8
  br label %25

25:                                               ; preds = %16
  %26 = load i32, ptr %8, align 4
  %27 = add nsw i32 %26, 1
  store i32 %27, ptr %8, align 4
  br label %12, !llvm.loop !7

28:                                               ; preds = %12
  %29 = load double, ptr %7, align 8
  ret double %29
}

; Function Attrs: nocallback nocreateundeforpoison nofree nosync nounwind speculatable willreturn memory(none)
declare double @llvm.fmuladd.f64(double, double, double) #1

; Function Attrs: noinline nounwind uwtable
define dso_local i32 @main() #0 {
  %1 = alloca i32, align 4
  %2 = alloca [5 x double], align 16
  %3 = alloca double, align 8
  store i32 0, ptr %1, align 4
  call void @llvm.memset.p0.i64(ptr align 16 %2, i8 0, i64 40, i1 false)
  %4 = getelementptr inbounds [5 x double], ptr %2, i32 0, i32 0
  store double 3.000000e+00, ptr %4, align 16
  %5 = getelementptr inbounds [5 x double], ptr %2, i32 0, i32 1
  store double -2.000000e+00, ptr %5, align 8
  %6 = getelementptr inbounds [5 x double], ptr %2, i32 0, i32 2
  store double 5.000000e+00, ptr %6, align 16
  %7 = getelementptr inbounds [5 x double], ptr %2, i32 0, i32 3
  store double -1.000000e+00, ptr %7, align 8
  %8 = getelementptr inbounds [5 x double], ptr %2, i32 0, i32 4
  store double 7.000000e+00, ptr %8, align 16
  %9 = getelementptr inbounds [5 x double], ptr %2, i64 0, i64 0
  %10 = call double @horner(ptr noundef %9, i32 noundef 4, double noundef 2.500000e+00)
  store double %10, ptr %3, align 8
  %11 = load double, ptr %3, align 8
  %12 = fptosi double %11 to i32
  %13 = and i32 %12, 255
  ret i32 %13
}

; Function Attrs: nocallback nofree nosync nounwind willreturn memory(argmem: write)
declare void @llvm.memset.p0.i64(ptr writeonly captures(none), i8, i64, i1 immarg) #2

attributes #0 = { noinline nounwind uwtable "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #1 = { nocallback nocreateundeforpoison nofree nosync nounwind speculatable willreturn memory(none) }
attributes #2 = { nocallback nofree nosync nounwind willreturn memory(argmem: write) }

!llvm.dbg.cu = !{!0}
!llvm.module.flags = !{!2, !3, !4, !5}
!llvm.ident = !{!6}

!0 = distinct !DICompileUnit(language: DW_LANG_C11, file: !1, producer: "clang version 23.1.2 (https://github.com/llvm/llvm-project 85ac560262434c9ccfc0c183ec22d4138ed647fb)", isOptimized: false, runtimeVersion: 0, emissionKind: NoDebug, splitDebugInlining: false, nameTableKind: None)
!1 = !DIFile(filename: "benchmarks\\test\\PG020_horner_eval.c", directory: "C:\\COMPILER PROJECT\\llvm-ml-pass-project")
!2 = !{i32 2, !"Debug Info Version", i32 3}
!3 = !{i32 8, !"PIC Level", i32 2}
!4 = !{i32 7, !"uwtable", i32 2}
!5 = !{i32 1, !"MaxTLSAlign", i32 65536}
!6 = !{!"clang version 23.1.2 (https://github.com/llvm/llvm-project 85ac560262434c9ccfc0c183ec22d4138ed647fb)"}
!7 = distinct !{!7, !8}
!8 = !{!"llvm.loop.mustprogress"}
