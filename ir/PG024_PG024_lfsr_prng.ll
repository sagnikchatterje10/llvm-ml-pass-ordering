; ModuleID = 'benchmarks/train/PG024_lfsr_prng.c'
source_filename = "benchmarks/train/PG024_lfsr_prng.c"
target datalayout = "e-m:w-p270:32:32-p271:32:32-p272:64:64-i64:64-i128:128-f80:128-n8:16:32:64-S128"
target triple = "x86_64-w64-windows-gnu"

; Function Attrs: noinline nounwind uwtable
define dso_local i32 @lfsr_step(ptr noundef %0) #0 {
  %2 = alloca ptr, align 8
  %3 = alloca i32, align 4
  store ptr %0, ptr %2, align 8
  %4 = load ptr, ptr %2, align 8
  %5 = load i32, ptr %4, align 4
  %6 = lshr i32 %5, 0
  %7 = load ptr, ptr %2, align 8
  %8 = load i32, ptr %7, align 4
  %9 = lshr i32 %8, 2
  %10 = xor i32 %6, %9
  %11 = load ptr, ptr %2, align 8
  %12 = load i32, ptr %11, align 4
  %13 = lshr i32 %12, 3
  %14 = xor i32 %10, %13
  %15 = load ptr, ptr %2, align 8
  %16 = load i32, ptr %15, align 4
  %17 = lshr i32 %16, 5
  %18 = xor i32 %14, %17
  %19 = and i32 %18, 1
  store i32 %19, ptr %3, align 4
  %20 = load ptr, ptr %2, align 8
  %21 = load i32, ptr %20, align 4
  %22 = lshr i32 %21, 1
  %23 = load i32, ptr %3, align 4
  %24 = shl i32 %23, 15
  %25 = or i32 %22, %24
  %26 = load ptr, ptr %2, align 8
  store i32 %25, ptr %26, align 4
  %27 = load ptr, ptr %2, align 8
  %28 = load i32, ptr %27, align 4
  ret i32 %28
}

; Function Attrs: noinline nounwind uwtable
define dso_local i32 @main() #0 {
  %1 = alloca i32, align 4
  %2 = alloca i32, align 4
  %3 = alloca i32, align 4
  %4 = alloca i32, align 4
  store i32 0, ptr %1, align 4
  store i32 44257, ptr %2, align 4
  store i32 0, ptr %3, align 4
  store i32 0, ptr %4, align 4
  br label %5

5:                                                ; preds = %12, %0
  %6 = load i32, ptr %4, align 4
  %7 = icmp slt i32 %6, 50
  br i1 %7, label %8, label %15

8:                                                ; preds = %5
  %9 = call i32 @lfsr_step(ptr noundef %2)
  %10 = load i32, ptr %3, align 4
  %11 = add i32 %10, %9
  store i32 %11, ptr %3, align 4
  br label %12

12:                                               ; preds = %8
  %13 = load i32, ptr %4, align 4
  %14 = add nsw i32 %13, 1
  store i32 %14, ptr %4, align 4
  br label %5, !llvm.loop !7

15:                                               ; preds = %5
  %16 = load i32, ptr %3, align 4
  %17 = and i32 %16, 255
  ret i32 %17
}

attributes #0 = { noinline nounwind uwtable "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }

!llvm.dbg.cu = !{!0}
!llvm.module.flags = !{!2, !3, !4, !5}
!llvm.ident = !{!6}

!0 = distinct !DICompileUnit(language: DW_LANG_C11, file: !1, producer: "clang version 23.1.2 (https://github.com/llvm/llvm-project 85ac560262434c9ccfc0c183ec22d4138ed647fb)", isOptimized: false, runtimeVersion: 0, emissionKind: NoDebug, splitDebugInlining: false, nameTableKind: None)
!1 = !DIFile(filename: "benchmarks/train\\PG024_lfsr_prng.c", directory: "C:\\COMPILER PROJECT\\llvm-ml-pass-project")
!2 = !{i32 2, !"Debug Info Version", i32 3}
!3 = !{i32 8, !"PIC Level", i32 2}
!4 = !{i32 7, !"uwtable", i32 2}
!5 = !{i32 1, !"MaxTLSAlign", i32 65536}
!6 = !{!"clang version 23.1.2 (https://github.com/llvm/llvm-project 85ac560262434c9ccfc0c183ec22d4138ed647fb)"}
!7 = distinct !{!7, !8}
!8 = !{!"llvm.loop.mustprogress"}
