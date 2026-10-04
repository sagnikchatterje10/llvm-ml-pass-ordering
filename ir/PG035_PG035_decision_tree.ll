; ModuleID = 'benchmarks/test/PG035_decision_tree.c'
source_filename = "benchmarks/test/PG035_decision_tree.c"
target datalayout = "e-m:w-p270:32:32-p271:32:32-p272:64:64-i64:64-i128:128-f80:128-n8:16:32:64-S128"
target triple = "x86_64-w64-windows-gnu"

; Function Attrs: noinline nounwind uwtable
define dso_local i32 @classify_point(i32 noundef %0, i32 noundef %1, i32 noundef %2) #0 {
  %4 = alloca i32, align 4
  %5 = alloca i32, align 4
  %6 = alloca i32, align 4
  %7 = alloca i32, align 4
  store i32 %0, ptr %5, align 4
  store i32 %1, ptr %6, align 4
  store i32 %2, ptr %7, align 4
  %8 = load i32, ptr %5, align 4
  %9 = icmp sgt i32 %8, 10
  br i1 %9, label %10, label %24

10:                                               ; preds = %3
  %11 = load i32, ptr %6, align 4
  %12 = icmp slt i32 %11, 20
  br i1 %12, label %13, label %18

13:                                               ; preds = %10
  %14 = load i32, ptr %7, align 4
  %15 = icmp sge i32 %14, 5
  br i1 %15, label %16, label %17

16:                                               ; preds = %13
  store i32 1, ptr %4, align 4
  br label %38

17:                                               ; preds = %13
  store i32 2, ptr %4, align 4
  br label %38

18:                                               ; preds = %10
  %19 = load i32, ptr %7, align 4
  %20 = srem i32 %19, 2
  %21 = icmp eq i32 %20, 0
  br i1 %21, label %22, label %23

22:                                               ; preds = %18
  store i32 3, ptr %4, align 4
  br label %38

23:                                               ; preds = %18
  store i32 4, ptr %4, align 4
  br label %38

24:                                               ; preds = %3
  %25 = load i32, ptr %6, align 4
  %26 = icmp sge i32 %25, 50
  br i1 %26, label %27, label %32

27:                                               ; preds = %24
  %28 = load i32, ptr %7, align 4
  %29 = icmp slt i32 %28, 0
  br i1 %29, label %30, label %31

30:                                               ; preds = %27
  store i32 5, ptr %4, align 4
  br label %38

31:                                               ; preds = %27
  store i32 6, ptr %4, align 4
  br label %38

32:                                               ; preds = %24
  %33 = load i32, ptr %5, align 4
  %34 = load i32, ptr %6, align 4
  %35 = icmp eq i32 %33, %34
  br i1 %35, label %36, label %37

36:                                               ; preds = %32
  store i32 7, ptr %4, align 4
  br label %38

37:                                               ; preds = %32
  store i32 8, ptr %4, align 4
  br label %38

38:                                               ; preds = %37, %36, %31, %30, %23, %22, %17, %16
  %39 = load i32, ptr %4, align 4
  ret i32 %39
}

; Function Attrs: noinline nounwind uwtable
define dso_local i32 @main() #0 {
  %1 = alloca i32, align 4
  %2 = alloca i32, align 4
  %3 = alloca i32, align 4
  %4 = alloca i32, align 4
  store i32 0, ptr %1, align 4
  %5 = call i32 @classify_point(i32 noundef 15, i32 noundef 10, i32 noundef 8)
  store i32 %5, ptr %2, align 4
  %6 = call i32 @classify_point(i32 noundef 5, i32 noundef 50, i32 noundef -3)
  store i32 %6, ptr %3, align 4
  %7 = call i32 @classify_point(i32 noundef 2, i32 noundef 2, i32 noundef 10)
  store i32 %7, ptr %4, align 4
  %8 = load i32, ptr %2, align 4
  %9 = load i32, ptr %3, align 4
  %10 = add nsw i32 %8, %9
  %11 = load i32, ptr %4, align 4
  %12 = add nsw i32 %10, %11
  ret i32 %12
}

attributes #0 = { noinline nounwind uwtable "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }

!llvm.dbg.cu = !{!0}
!llvm.module.flags = !{!2, !3, !4, !5}
!llvm.ident = !{!6}

!0 = distinct !DICompileUnit(language: DW_LANG_C11, file: !1, producer: "clang version 23.1.2 (https://github.com/llvm/llvm-project 85ac560262434c9ccfc0c183ec22d4138ed647fb)", isOptimized: false, runtimeVersion: 0, emissionKind: NoDebug, splitDebugInlining: false, nameTableKind: None)
!1 = !DIFile(filename: "benchmarks/test\\PG035_decision_tree.c", directory: "C:\\COMPILER PROJECT\\llvm-ml-pass-project")
!2 = !{i32 2, !"Debug Info Version", i32 3}
!3 = !{i32 8, !"PIC Level", i32 2}
!4 = !{i32 7, !"uwtable", i32 2}
!5 = !{i32 1, !"MaxTLSAlign", i32 65536}
!6 = !{!"clang version 23.1.2 (https://github.com/llvm/llvm-project 85ac560262434c9ccfc0c183ec22d4138ed647fb)"}
