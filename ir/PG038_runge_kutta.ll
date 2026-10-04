; ModuleID = 'benchmarks\train\PG038_runge_kutta.c'
source_filename = "benchmarks\\train\\PG038_runge_kutta.c"
target datalayout = "e-m:w-p270:32:32-p271:32:32-p272:64:64-i64:64-i128:128-f80:128-n8:16:32:64-S128"
target triple = "x86_64-w64-windows-gnu"

; Function Attrs: noinline nounwind uwtable
define dso_local double @rk2_integrate(double noundef %0, double noundef %1, double noundef %2, i32 noundef %3) #0 {
  %5 = alloca double, align 8
  %6 = alloca double, align 8
  %7 = alloca double, align 8
  %8 = alloca i32, align 4
  %9 = alloca double, align 8
  %10 = alloca double, align 8
  %11 = alloca i32, align 4
  %12 = alloca double, align 8
  %13 = alloca double, align 8
  store double %0, ptr %5, align 8
  store double %1, ptr %6, align 8
  store double %2, ptr %7, align 8
  store i32 %3, ptr %8, align 4
  %14 = load double, ptr %5, align 8
  store double %14, ptr %9, align 8
  %15 = load double, ptr %6, align 8
  store double %15, ptr %10, align 8
  store i32 0, ptr %11, align 4
  br label %16

16:                                               ; preds = %43, %4
  %17 = load i32, ptr %11, align 4
  %18 = load i32, ptr %8, align 4
  %19 = icmp slt i32 %17, %18
  br i1 %19, label %20, label %46

20:                                               ; preds = %16
  %21 = load double, ptr %7, align 8
  %22 = load double, ptr %9, align 8
  %23 = load double, ptr %10, align 8
  %24 = call double @f(double noundef %22, double noundef %23)
  %25 = fmul double %21, %24
  store double %25, ptr %12, align 8
  %26 = load double, ptr %7, align 8
  %27 = load double, ptr %9, align 8
  %28 = load double, ptr %7, align 8
  %29 = fadd double %27, %28
  %30 = load double, ptr %10, align 8
  %31 = load double, ptr %12, align 8
  %32 = fadd double %30, %31
  %33 = call double @f(double noundef %29, double noundef %32)
  %34 = fmul double %26, %33
  store double %34, ptr %13, align 8
  %35 = load double, ptr %12, align 8
  %36 = load double, ptr %13, align 8
  %37 = fadd double %35, %36
  %38 = load double, ptr %10, align 8
  %39 = call double @llvm.fmuladd.f64(double 5.000000e-01, double %37, double %38)
  store double %39, ptr %10, align 8
  %40 = load double, ptr %7, align 8
  %41 = load double, ptr %9, align 8
  %42 = fadd double %41, %40
  store double %42, ptr %9, align 8
  br label %43

43:                                               ; preds = %20
  %44 = load i32, ptr %11, align 4
  %45 = add nsw i32 %44, 1
  store i32 %45, ptr %11, align 4
  br label %16, !llvm.loop !7

46:                                               ; preds = %16
  %47 = load double, ptr %10, align 8
  ret double %47
}

; Function Attrs: noinline nounwind uwtable
define internal double @f(double noundef %0, double noundef %1) #0 {
  %3 = alloca double, align 8
  %4 = alloca double, align 8
  store double %0, ptr %3, align 8
  store double %1, ptr %4, align 8
  %5 = load double, ptr %3, align 8
  %6 = load double, ptr %4, align 8
  %7 = load double, ptr %4, align 8
  %8 = fmul double 5.000000e-01, %7
  %9 = load double, ptr %4, align 8
  %10 = fmul double %8, %9
  %11 = fneg double %10
  %12 = call double @llvm.fmuladd.f64(double %5, double %6, double %11)
  ret double %12
}

; Function Attrs: nocallback nocreateundeforpoison nofree nosync nounwind speculatable willreturn memory(none)
declare double @llvm.fmuladd.f64(double, double, double) #1

; Function Attrs: noinline nounwind uwtable
define dso_local i32 @main() #0 {
  %1 = alloca i32, align 4
  %2 = alloca double, align 8
  store i32 0, ptr %1, align 4
  %3 = call double @rk2_integrate(double noundef 0.000000e+00, double noundef 1.000000e+00, double noundef 5.000000e-02, i32 noundef 20)
  store double %3, ptr %2, align 8
  %4 = load double, ptr %2, align 8
  %5 = fmul double %4, 1.000000e+01
  %6 = fptosi double %5 to i32
  %7 = and i32 %6, 255
  ret i32 %7
}

attributes #0 = { noinline nounwind uwtable "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #1 = { nocallback nocreateundeforpoison nofree nosync nounwind speculatable willreturn memory(none) }

!llvm.dbg.cu = !{!0}
!llvm.module.flags = !{!2, !3, !4, !5}
!llvm.ident = !{!6}

!0 = distinct !DICompileUnit(language: DW_LANG_C11, file: !1, producer: "clang version 23.1.2 (https://github.com/llvm/llvm-project 85ac560262434c9ccfc0c183ec22d4138ed647fb)", isOptimized: false, runtimeVersion: 0, emissionKind: NoDebug, splitDebugInlining: false, nameTableKind: None)
!1 = !DIFile(filename: "benchmarks\\train\\PG038_runge_kutta.c", directory: "C:\\COMPILER PROJECT\\llvm-ml-pass-project")
!2 = !{i32 2, !"Debug Info Version", i32 3}
!3 = !{i32 8, !"PIC Level", i32 2}
!4 = !{i32 7, !"uwtable", i32 2}
!5 = !{i32 1, !"MaxTLSAlign", i32 65536}
!6 = !{!"clang version 23.1.2 (https://github.com/llvm/llvm-project 85ac560262434c9ccfc0c183ec22d4138ed647fb)"}
!7 = distinct !{!7, !8}
!8 = !{!"llvm.loop.mustprogress"}
