; ModuleID = 'benchmarks/val/PG029_linked_list.c'
source_filename = "benchmarks/val/PG029_linked_list.c"
target datalayout = "e-m:w-p270:32:32-p271:32:32-p272:64:64-i64:64-i128:128-f80:128-n8:16:32:64-S128"
target triple = "x86_64-w64-windows-gnu"

%struct.Node = type { i32, i32 }

@__const.main.pool = private unnamed_addr constant [6 x %struct.Node] [%struct.Node { i32 10, i32 1 }, %struct.Node { i32 25, i32 2 }, %struct.Node { i32 5, i32 3 }, %struct.Node { i32 40, i32 4 }, %struct.Node { i32 15, i32 5 }, %struct.Node { i32 30, i32 -1 }], align 16

; Function Attrs: noinline nounwind uwtable
define dso_local i32 @filter_sum(ptr noundef %0, i32 noundef %1, i32 noundef %2) #0 {
  %4 = alloca ptr, align 8
  %5 = alloca i32, align 4
  %6 = alloca i32, align 4
  %7 = alloca i32, align 4
  %8 = alloca i32, align 4
  store ptr %0, ptr %4, align 8
  store i32 %1, ptr %5, align 4
  store i32 %2, ptr %6, align 4
  store i32 0, ptr %7, align 4
  %9 = load i32, ptr %5, align 4
  store i32 %9, ptr %8, align 4
  br label %10

10:                                               ; preds = %31, %3
  %11 = load i32, ptr %8, align 4
  %12 = icmp sge i32 %11, 0
  br i1 %12, label %13, label %38

13:                                               ; preds = %10
  %14 = load ptr, ptr %4, align 8
  %15 = load i32, ptr %8, align 4
  %16 = sext i32 %15 to i64
  %17 = getelementptr inbounds %struct.Node, ptr %14, i64 %16
  %18 = getelementptr inbounds nuw %struct.Node, ptr %17, i32 0, i32 0
  %19 = load i32, ptr %18, align 4
  %20 = load i32, ptr %6, align 4
  %21 = icmp sgt i32 %19, %20
  br i1 %21, label %22, label %31

22:                                               ; preds = %13
  %23 = load ptr, ptr %4, align 8
  %24 = load i32, ptr %8, align 4
  %25 = sext i32 %24 to i64
  %26 = getelementptr inbounds %struct.Node, ptr %23, i64 %25
  %27 = getelementptr inbounds nuw %struct.Node, ptr %26, i32 0, i32 0
  %28 = load i32, ptr %27, align 4
  %29 = load i32, ptr %7, align 4
  %30 = add nsw i32 %29, %28
  store i32 %30, ptr %7, align 4
  br label %31

31:                                               ; preds = %22, %13
  %32 = load ptr, ptr %4, align 8
  %33 = load i32, ptr %8, align 4
  %34 = sext i32 %33 to i64
  %35 = getelementptr inbounds %struct.Node, ptr %32, i64 %34
  %36 = getelementptr inbounds nuw %struct.Node, ptr %35, i32 0, i32 1
  %37 = load i32, ptr %36, align 4
  store i32 %37, ptr %8, align 4
  br label %10, !llvm.loop !7

38:                                               ; preds = %10
  %39 = load i32, ptr %7, align 4
  ret i32 %39
}

; Function Attrs: noinline nounwind uwtable
define dso_local i32 @main() #0 {
  %1 = alloca i32, align 4
  %2 = alloca [6 x %struct.Node], align 16
  %3 = alloca i32, align 4
  store i32 0, ptr %1, align 4
  call void @llvm.memcpy.p0.p0.i64(ptr align 16 %2, ptr align 16 @__const.main.pool, i64 48, i1 false)
  %4 = getelementptr inbounds [6 x %struct.Node], ptr %2, i64 0, i64 0
  %5 = call i32 @filter_sum(ptr noundef %4, i32 noundef 0, i32 noundef 15)
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
!1 = !DIFile(filename: "benchmarks/val\\PG029_linked_list.c", directory: "C:\\COMPILER PROJECT\\llvm-ml-pass-project")
!2 = !{i32 2, !"Debug Info Version", i32 3}
!3 = !{i32 8, !"PIC Level", i32 2}
!4 = !{i32 7, !"uwtable", i32 2}
!5 = !{i32 1, !"MaxTLSAlign", i32 65536}
!6 = !{!"clang version 23.1.2 (https://github.com/llvm/llvm-project 85ac560262434c9ccfc0c183ec22d4138ed647fb)"}
!7 = distinct !{!7, !8}
!8 = !{!"llvm.loop.mustprogress"}
