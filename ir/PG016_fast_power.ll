; ModuleID = 'benchmarks\train\PG016_fast_power.c'
source_filename = "benchmarks\\train\\PG016_fast_power.c"
target datalayout = "e-m:w-p270:32:32-p271:32:32-p272:64:64-i64:64-i128:128-f80:128-n8:16:32:64-S128"
target triple = "x86_64-w64-windows-gnu"

; Function Attrs: noinline nounwind uwtable
define dso_local i64 @mod_pow(i64 noundef %0, i64 noundef %1, i64 noundef %2) #0 {
  %4 = alloca i64, align 8
  %5 = alloca i64, align 8
  %6 = alloca i64, align 8
  %7 = alloca i64, align 8
  store i64 %0, ptr %4, align 8
  store i64 %1, ptr %5, align 8
  store i64 %2, ptr %6, align 8
  store i64 1, ptr %7, align 8
  %8 = load i64, ptr %6, align 8
  %9 = load i64, ptr %4, align 8
  %10 = srem i64 %9, %8
  store i64 %10, ptr %4, align 8
  br label %11

11:                                               ; preds = %24, %3
  %12 = load i64, ptr %5, align 8
  %13 = icmp sgt i64 %12, 0
  br i1 %13, label %14, label %32

14:                                               ; preds = %11
  %15 = load i64, ptr %5, align 8
  %16 = and i64 %15, 1
  %17 = icmp ne i64 %16, 0
  br i1 %17, label %18, label %24

18:                                               ; preds = %14
  %19 = load i64, ptr %7, align 8
  %20 = load i64, ptr %4, align 8
  %21 = mul nsw i64 %19, %20
  %22 = load i64, ptr %6, align 8
  %23 = srem i64 %21, %22
  store i64 %23, ptr %7, align 8
  br label %24

24:                                               ; preds = %18, %14
  %25 = load i64, ptr %4, align 8
  %26 = load i64, ptr %4, align 8
  %27 = mul nsw i64 %25, %26
  %28 = load i64, ptr %6, align 8
  %29 = srem i64 %27, %28
  store i64 %29, ptr %4, align 8
  %30 = load i64, ptr %5, align 8
  %31 = ashr i64 %30, 1
  store i64 %31, ptr %5, align 8
  br label %11, !llvm.loop !7

32:                                               ; preds = %11
  %33 = load i64, ptr %7, align 8
  ret i64 %33
}

; Function Attrs: noinline nounwind uwtable
define dso_local i32 @main() #0 {
  %1 = alloca i32, align 4
  %2 = alloca i64, align 8
  store i32 0, ptr %1, align 4
  %3 = call i64 @mod_pow(i64 noundef 7, i64 noundef 25, i64 noundef 1000000007)
  store i64 %3, ptr %2, align 8
  %4 = load i64, ptr %2, align 8
  %5 = and i64 %4, 255
  %6 = trunc i64 %5 to i32
  ret i32 %6
}

attributes #0 = { noinline nounwind uwtable "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }

!llvm.dbg.cu = !{!0}
!llvm.module.flags = !{!2, !3, !4, !5}
!llvm.ident = !{!6}

!0 = distinct !DICompileUnit(language: DW_LANG_C11, file: !1, producer: "clang version 23.1.2 (https://github.com/llvm/llvm-project 85ac560262434c9ccfc0c183ec22d4138ed647fb)", isOptimized: false, runtimeVersion: 0, emissionKind: NoDebug, splitDebugInlining: false, nameTableKind: None)
!1 = !DIFile(filename: "benchmarks\\train\\PG016_fast_power.c", directory: "C:\\COMPILER PROJECT\\llvm-ml-pass-project")
!2 = !{i32 2, !"Debug Info Version", i32 3}
!3 = !{i32 8, !"PIC Level", i32 2}
!4 = !{i32 7, !"uwtable", i32 2}
!5 = !{i32 1, !"MaxTLSAlign", i32 65536}
!6 = !{!"clang version 23.1.2 (https://github.com/llvm/llvm-project 85ac560262434c9ccfc0c183ec22d4138ed647fb)"}
!7 = distinct !{!7, !8}
!8 = !{!"llvm.loop.mustprogress"}
