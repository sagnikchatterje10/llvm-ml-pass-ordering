; ModuleID = 'benchmarks\train\PG019_sqrt_newton.c'
source_filename = "benchmarks\\train\\PG019_sqrt_newton.c"
target datalayout = "e-m:w-p270:32:32-p271:32:32-p272:64:64-i64:64-i128:128-f80:128-n8:16:32:64-S128"
target triple = "x86_64-w64-windows-gnu"

; Function Attrs: noinline nounwind uwtable
define dso_local double @sqrt_newton(double noundef %0) #0 {
  %2 = alloca double, align 8
  %3 = alloca double, align 8
  %4 = alloca double, align 8
  %5 = alloca i32, align 4
  %6 = alloca double, align 8
  %7 = alloca double, align 8
  store double %0, ptr %3, align 8
  %8 = load double, ptr %3, align 8
  %9 = fcmp olt double %8, 0.000000e+00
  br i1 %9, label %10, label %11

10:                                               ; preds = %1
  store double -1.000000e+00, ptr %2, align 8
  br label %47

11:                                               ; preds = %1
  %12 = load double, ptr %3, align 8
  %13 = fcmp oeq double %12, 0.000000e+00
  br i1 %13, label %14, label %15

14:                                               ; preds = %11
  store double 0.000000e+00, ptr %2, align 8
  br label %47

15:                                               ; preds = %11
  %16 = load double, ptr %3, align 8
  store double %16, ptr %4, align 8
  store i32 0, ptr %5, align 4
  br label %17

17:                                               ; preds = %42, %15
  %18 = load i32, ptr %5, align 4
  %19 = icmp slt i32 %18, 20
  br i1 %19, label %20, label %45

20:                                               ; preds = %17
  %21 = load double, ptr %4, align 8
  %22 = load double, ptr %3, align 8
  %23 = load double, ptr %4, align 8
  %24 = fdiv double %22, %23
  %25 = fadd double %21, %24
  %26 = fmul double 5.000000e-01, %25
  store double %26, ptr %6, align 8
  %27 = load double, ptr %6, align 8
  %28 = load double, ptr %4, align 8
  %29 = fsub double %27, %28
  store double %29, ptr %7, align 8
  %30 = load double, ptr %7, align 8
  %31 = fcmp olt double %30, 0.000000e+00
  br i1 %31, label %32, label %35

32:                                               ; preds = %20
  %33 = load double, ptr %7, align 8
  %34 = fneg double %33
  store double %34, ptr %7, align 8
  br label %35

35:                                               ; preds = %32, %20
  %36 = load double, ptr %7, align 8
  %37 = fcmp olt double %36, f0x3EB0C6F7A0B5ED8D
  br i1 %37, label %38, label %40

38:                                               ; preds = %35
  %39 = load double, ptr %6, align 8
  store double %39, ptr %2, align 8
  br label %47

40:                                               ; preds = %35
  %41 = load double, ptr %6, align 8
  store double %41, ptr %4, align 8
  br label %42

42:                                               ; preds = %40
  %43 = load i32, ptr %5, align 4
  %44 = add nsw i32 %43, 1
  store i32 %44, ptr %5, align 4
  br label %17, !llvm.loop !7

45:                                               ; preds = %17
  %46 = load double, ptr %4, align 8
  store double %46, ptr %2, align 8
  br label %47

47:                                               ; preds = %45, %38, %14, %10
  %48 = load double, ptr %2, align 8
  ret double %48
}

; Function Attrs: noinline nounwind uwtable
define dso_local i32 @main() #0 {
  %1 = alloca i32, align 4
  %2 = alloca double, align 8
  store i32 0, ptr %1, align 4
  %3 = call double @sqrt_newton(double noundef 2.560000e+02)
  store double %3, ptr %2, align 8
  %4 = load double, ptr %2, align 8
  %5 = fptosi double %4 to i32
  ret i32 %5
}

attributes #0 = { noinline nounwind uwtable "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }

!llvm.dbg.cu = !{!0}
!llvm.module.flags = !{!2, !3, !4, !5}
!llvm.ident = !{!6}

!0 = distinct !DICompileUnit(language: DW_LANG_C11, file: !1, producer: "clang version 23.1.2 (https://github.com/llvm/llvm-project 85ac560262434c9ccfc0c183ec22d4138ed647fb)", isOptimized: false, runtimeVersion: 0, emissionKind: NoDebug, splitDebugInlining: false, nameTableKind: None)
!1 = !DIFile(filename: "benchmarks\\train\\PG019_sqrt_newton.c", directory: "C:\\COMPILER PROJECT\\llvm-ml-pass-project")
!2 = !{i32 2, !"Debug Info Version", i32 3}
!3 = !{i32 8, !"PIC Level", i32 2}
!4 = !{i32 7, !"uwtable", i32 2}
!5 = !{i32 1, !"MaxTLSAlign", i32 65536}
!6 = !{!"clang version 23.1.2 (https://github.com/llvm/llvm-project 85ac560262434c9ccfc0c183ec22d4138ed647fb)"}
!7 = distinct !{!7, !8}
!8 = !{!"llvm.loop.mustprogress"}
