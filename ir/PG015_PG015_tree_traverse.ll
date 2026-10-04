; ModuleID = 'benchmarks/test/PG015_tree_traverse.c'
source_filename = "benchmarks/test/PG015_tree_traverse.c"
target datalayout = "e-m:w-p270:32:32-p271:32:32-p272:64:64-i64:64-i128:128-f80:128-n8:16:32:64-S128"
target triple = "x86_64-w64-windows-gnu"

%struct.TreeNode = type { i32, i32, i32 }

@__const.main.nodes = private unnamed_addr constant [5 x %struct.TreeNode] [%struct.TreeNode { i32 10, i32 1, i32 2 }, %struct.TreeNode { i32 5, i32 3, i32 4 }, %struct.TreeNode { i32 15, i32 -1, i32 -1 }, %struct.TreeNode { i32 2, i32 -1, i32 -1 }, %struct.TreeNode { i32 7, i32 -1, i32 -1 }], align 16

; Function Attrs: noinline nounwind uwtable
define dso_local i32 @tree_sum(ptr noundef %0, i32 noundef %1) #0 {
  %3 = alloca i32, align 4
  %4 = alloca ptr, align 8
  %5 = alloca i32, align 4
  %6 = alloca i32, align 4
  store ptr %0, ptr %4, align 8
  store i32 %1, ptr %5, align 4
  %7 = load i32, ptr %5, align 4
  %8 = icmp slt i32 %7, 0
  br i1 %8, label %9, label %10

9:                                                ; preds = %2
  store i32 0, ptr %3, align 4
  br label %38

10:                                               ; preds = %2
  %11 = load ptr, ptr %4, align 8
  %12 = load i32, ptr %5, align 4
  %13 = sext i32 %12 to i64
  %14 = getelementptr inbounds %struct.TreeNode, ptr %11, i64 %13
  %15 = getelementptr inbounds nuw %struct.TreeNode, ptr %14, i32 0, i32 0
  %16 = load i32, ptr %15, align 4
  store i32 %16, ptr %6, align 4
  %17 = load ptr, ptr %4, align 8
  %18 = load ptr, ptr %4, align 8
  %19 = load i32, ptr %5, align 4
  %20 = sext i32 %19 to i64
  %21 = getelementptr inbounds %struct.TreeNode, ptr %18, i64 %20
  %22 = getelementptr inbounds nuw %struct.TreeNode, ptr %21, i32 0, i32 1
  %23 = load i32, ptr %22, align 4
  %24 = call i32 @tree_sum(ptr noundef %17, i32 noundef %23)
  %25 = load i32, ptr %6, align 4
  %26 = add nsw i32 %25, %24
  store i32 %26, ptr %6, align 4
  %27 = load ptr, ptr %4, align 8
  %28 = load ptr, ptr %4, align 8
  %29 = load i32, ptr %5, align 4
  %30 = sext i32 %29 to i64
  %31 = getelementptr inbounds %struct.TreeNode, ptr %28, i64 %30
  %32 = getelementptr inbounds nuw %struct.TreeNode, ptr %31, i32 0, i32 2
  %33 = load i32, ptr %32, align 4
  %34 = call i32 @tree_sum(ptr noundef %27, i32 noundef %33)
  %35 = load i32, ptr %6, align 4
  %36 = add nsw i32 %35, %34
  store i32 %36, ptr %6, align 4
  %37 = load i32, ptr %6, align 4
  store i32 %37, ptr %3, align 4
  br label %38

38:                                               ; preds = %10, %9
  %39 = load i32, ptr %3, align 4
  ret i32 %39
}

; Function Attrs: noinline nounwind uwtable
define dso_local i32 @main() #0 {
  %1 = alloca i32, align 4
  %2 = alloca [5 x %struct.TreeNode], align 16
  %3 = alloca i32, align 4
  store i32 0, ptr %1, align 4
  call void @llvm.memcpy.p0.p0.i64(ptr align 16 %2, ptr align 16 @__const.main.nodes, i64 60, i1 false)
  %4 = getelementptr inbounds [5 x %struct.TreeNode], ptr %2, i64 0, i64 0
  %5 = call i32 @tree_sum(ptr noundef %4, i32 noundef 0)
  store i32 %5, ptr %3, align 4
  %6 = load i32, ptr %3, align 4
  %7 = and i32 %6, 255
  ret i32 %7
}

; Function Attrs: nocallback nofree nosync nounwind willreturn memory(argmem: readwrite)
declare void @llvm.memcpy.p0.p0.i64(ptr noalias writeonly captures(none), ptr noalias readonly captures(none), i64, i1 immarg) #1

attributes #0 = { noinline nounwind uwtable "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #1 = { nocallback nofree nosync nounwind willreturn memory(argmem: readwrite) }

!llvm.dbg.cu = !{!0}
!llvm.module.flags = !{!2, !3, !4, !5}
!llvm.ident = !{!6}

!0 = distinct !DICompileUnit(language: DW_LANG_C11, file: !1, producer: "clang version 23.1.2 (https://github.com/llvm/llvm-project 85ac560262434c9ccfc0c183ec22d4138ed647fb)", isOptimized: false, runtimeVersion: 0, emissionKind: NoDebug, splitDebugInlining: false, nameTableKind: None)
!1 = !DIFile(filename: "benchmarks/test\\PG015_tree_traverse.c", directory: "C:\\COMPILER PROJECT\\llvm-ml-pass-project")
!2 = !{i32 2, !"Debug Info Version", i32 3}
!3 = !{i32 8, !"PIC Level", i32 2}
!4 = !{i32 7, !"uwtable", i32 2}
!5 = !{i32 1, !"MaxTLSAlign", i32 65536}
!6 = !{!"clang version 23.1.2 (https://github.com/llvm/llvm-project 85ac560262434c9ccfc0c183ec22d4138ed647fb)"}
