; ModuleID = 'benchmarks\train\PG013_hanoi.c'
source_filename = "benchmarks\\train\\PG013_hanoi.c"
target datalayout = "e-m:w-p270:32:32-p271:32:32-p272:64:64-i64:64-i128:128-f80:128-n8:16:32:64-S128"
target triple = "x86_64-w64-windows-gnu"

; Function Attrs: noinline nounwind uwtable
define dso_local i32 @hanoi_moves(i32 noundef %0, i8 noundef %1, i8 noundef %2, i8 noundef %3) #0 {
  %5 = alloca i32, align 4
  %6 = alloca i32, align 4
  %7 = alloca i8, align 1
  %8 = alloca i8, align 1
  %9 = alloca i8, align 1
  %10 = alloca i32, align 4
  store i32 %0, ptr %6, align 4
  store i8 %1, ptr %7, align 1
  store i8 %2, ptr %8, align 1
  store i8 %3, ptr %9, align 1
  %11 = load i32, ptr %6, align 4
  %12 = icmp eq i32 %11, 1
  br i1 %12, label %13, label %14

13:                                               ; preds = %4
  store i32 1, ptr %5, align 4
  br label %32

14:                                               ; preds = %4
  %15 = load i32, ptr %6, align 4
  %16 = sub nsw i32 %15, 1
  %17 = load i8, ptr %7, align 1
  %18 = load i8, ptr %9, align 1
  %19 = load i8, ptr %8, align 1
  %20 = call i32 @hanoi_moves(i32 noundef %16, i8 noundef %17, i8 noundef %18, i8 noundef %19)
  store i32 %20, ptr %10, align 4
  %21 = load i32, ptr %10, align 4
  %22 = add nsw i32 %21, 1
  store i32 %22, ptr %10, align 4
  %23 = load i32, ptr %6, align 4
  %24 = sub nsw i32 %23, 1
  %25 = load i8, ptr %9, align 1
  %26 = load i8, ptr %8, align 1
  %27 = load i8, ptr %7, align 1
  %28 = call i32 @hanoi_moves(i32 noundef %24, i8 noundef %25, i8 noundef %26, i8 noundef %27)
  %29 = load i32, ptr %10, align 4
  %30 = add nsw i32 %29, %28
  store i32 %30, ptr %10, align 4
  %31 = load i32, ptr %10, align 4
  store i32 %31, ptr %5, align 4
  br label %32

32:                                               ; preds = %14, %13
  %33 = load i32, ptr %5, align 4
  ret i32 %33
}

; Function Attrs: noinline nounwind uwtable
define dso_local i32 @main() #0 {
  %1 = alloca i32, align 4
  %2 = alloca i32, align 4
  store i32 0, ptr %1, align 4
  %3 = call i32 @hanoi_moves(i32 noundef 5, i8 noundef 65, i8 noundef 67, i8 noundef 66)
  store i32 %3, ptr %2, align 4
  %4 = load i32, ptr %2, align 4
  %5 = and i32 %4, 127
  ret i32 %5
}

attributes #0 = { noinline nounwind uwtable "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }

!llvm.dbg.cu = !{!0}
!llvm.module.flags = !{!2, !3, !4, !5}
!llvm.ident = !{!6}

!0 = distinct !DICompileUnit(language: DW_LANG_C11, file: !1, producer: "clang version 23.1.2 (https://github.com/llvm/llvm-project 85ac560262434c9ccfc0c183ec22d4138ed647fb)", isOptimized: false, runtimeVersion: 0, emissionKind: NoDebug, splitDebugInlining: false, nameTableKind: None)
!1 = !DIFile(filename: "benchmarks\\train\\PG013_hanoi.c", directory: "C:\\COMPILER PROJECT\\llvm-ml-pass-project")
!2 = !{i32 2, !"Debug Info Version", i32 3}
!3 = !{i32 8, !"PIC Level", i32 2}
!4 = !{i32 7, !"uwtable", i32 2}
!5 = !{i32 1, !"MaxTLSAlign", i32 65536}
!6 = !{!"clang version 23.1.2 (https://github.com/llvm/llvm-project 85ac560262434c9ccfc0c183ec22d4138ed647fb)"}
