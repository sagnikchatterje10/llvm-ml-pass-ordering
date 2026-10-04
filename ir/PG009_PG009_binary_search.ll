; ModuleID = 'benchmarks/train/PG009_binary_search.c'
source_filename = "benchmarks/train/PG009_binary_search.c"
target datalayout = "e-m:w-p270:32:32-p271:32:32-p272:64:64-i64:64-i128:128-f80:128-n8:16:32:64-S128"
target triple = "x86_64-w64-windows-gnu"

@__const.main.sorted = private unnamed_addr constant [16 x i32] [i32 2, i32 5, i32 8, i32 12, i32 16, i32 23, i32 38, i32 56, i32 72, i32 91, i32 100, i32 120, i32 135, i32 140, i32 150, i32 160], align 16

; Function Attrs: noinline nounwind uwtable
define dso_local i32 @binary_search(ptr noundef %0, i32 noundef %1, i32 noundef %2) #0 {
  %4 = alloca i32, align 4
  %5 = alloca ptr, align 8
  %6 = alloca i32, align 4
  %7 = alloca i32, align 4
  %8 = alloca i32, align 4
  %9 = alloca i32, align 4
  %10 = alloca i32, align 4
  store ptr %0, ptr %5, align 8
  store i32 %1, ptr %6, align 4
  store i32 %2, ptr %7, align 4
  store i32 0, ptr %8, align 4
  %11 = load i32, ptr %6, align 4
  %12 = sub nsw i32 %11, 1
  store i32 %12, ptr %9, align 4
  br label %13

13:                                               ; preds = %47, %3
  %14 = load i32, ptr %8, align 4
  %15 = load i32, ptr %9, align 4
  %16 = icmp sle i32 %14, %15
  br i1 %16, label %17, label %48

17:                                               ; preds = %13
  %18 = load i32, ptr %8, align 4
  %19 = load i32, ptr %9, align 4
  %20 = load i32, ptr %8, align 4
  %21 = sub nsw i32 %19, %20
  %22 = sdiv i32 %21, 2
  %23 = add nsw i32 %18, %22
  store i32 %23, ptr %10, align 4
  %24 = load ptr, ptr %5, align 8
  %25 = load i32, ptr %10, align 4
  %26 = sext i32 %25 to i64
  %27 = getelementptr inbounds i32, ptr %24, i64 %26
  %28 = load i32, ptr %27, align 4
  %29 = load i32, ptr %7, align 4
  %30 = icmp eq i32 %28, %29
  br i1 %30, label %31, label %33

31:                                               ; preds = %17
  %32 = load i32, ptr %10, align 4
  store i32 %32, ptr %4, align 4
  br label %49

33:                                               ; preds = %17
  %34 = load ptr, ptr %5, align 8
  %35 = load i32, ptr %10, align 4
  %36 = sext i32 %35 to i64
  %37 = getelementptr inbounds i32, ptr %34, i64 %36
  %38 = load i32, ptr %37, align 4
  %39 = load i32, ptr %7, align 4
  %40 = icmp slt i32 %38, %39
  br i1 %40, label %41, label %44

41:                                               ; preds = %33
  %42 = load i32, ptr %10, align 4
  %43 = add nsw i32 %42, 1
  store i32 %43, ptr %8, align 4
  br label %47

44:                                               ; preds = %33
  %45 = load i32, ptr %10, align 4
  %46 = sub nsw i32 %45, 1
  store i32 %46, ptr %9, align 4
  br label %47

47:                                               ; preds = %44, %41
  br label %13, !llvm.loop !7

48:                                               ; preds = %13
  store i32 -1, ptr %4, align 4
  br label %49

49:                                               ; preds = %48, %31
  %50 = load i32, ptr %4, align 4
  ret i32 %50
}

; Function Attrs: noinline nounwind uwtable
define dso_local i32 @main() #0 {
  %1 = alloca i32, align 4
  %2 = alloca [16 x i32], align 16
  %3 = alloca i32, align 4
  %4 = alloca i32, align 4
  store i32 0, ptr %1, align 4
  call void @llvm.memcpy.p0.p0.i64(ptr align 16 %2, ptr align 16 @__const.main.sorted, i64 64, i1 false)
  %5 = getelementptr inbounds [16 x i32], ptr %2, i64 0, i64 0
  %6 = call i32 @binary_search(ptr noundef %5, i32 noundef 16, i32 noundef 23)
  store i32 %6, ptr %3, align 4
  %7 = getelementptr inbounds [16 x i32], ptr %2, i64 0, i64 0
  %8 = call i32 @binary_search(ptr noundef %7, i32 noundef 16, i32 noundef 999)
  store i32 %8, ptr %4, align 4
  %9 = load i32, ptr %3, align 4
  %10 = load i32, ptr %4, align 4
  %11 = icmp eq i32 %10, -1
  %12 = zext i1 %11 to i64
  %13 = select i1 %11, i32 1, i32 0
  %14 = add nsw i32 %9, %13
  ret i32 %14
}

; Function Attrs: nocallback nofree nosync nounwind willreturn memory(argmem: readwrite)
declare void @llvm.memcpy.p0.p0.i64(ptr noalias writeonly captures(none), ptr noalias readonly captures(none), i64, i1 immarg) #1

attributes #0 = { noinline nounwind uwtable "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #1 = { nocallback nofree nosync nounwind willreturn memory(argmem: readwrite) }

!llvm.dbg.cu = !{!0}
!llvm.module.flags = !{!2, !3, !4, !5}
!llvm.ident = !{!6}

!0 = distinct !DICompileUnit(language: DW_LANG_C11, file: !1, producer: "clang version 23.1.2 (https://github.com/llvm/llvm-project 85ac560262434c9ccfc0c183ec22d4138ed647fb)", isOptimized: false, runtimeVersion: 0, emissionKind: NoDebug, splitDebugInlining: false, nameTableKind: None)
!1 = !DIFile(filename: "benchmarks/train\\PG009_binary_search.c", directory: "C:\\COMPILER PROJECT\\llvm-ml-pass-project")
!2 = !{i32 2, !"Debug Info Version", i32 3}
!3 = !{i32 8, !"PIC Level", i32 2}
!4 = !{i32 7, !"uwtable", i32 2}
!5 = !{i32 1, !"MaxTLSAlign", i32 65536}
!6 = !{!"clang version 23.1.2 (https://github.com/llvm/llvm-project 85ac560262434c9ccfc0c183ec22d4138ed647fb)"}
!7 = distinct !{!7, !8}
!8 = !{!"llvm.loop.mustprogress"}
