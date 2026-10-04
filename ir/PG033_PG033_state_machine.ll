; ModuleID = 'benchmarks/val/PG033_state_machine.c'
source_filename = "benchmarks/val/PG033_state_machine.c"
target datalayout = "e-m:w-p270:32:32-p271:32:32-p272:64:64-i64:64-i128:128-f80:128-n8:16:32:64-S128"
target triple = "x86_64-w64-windows-gnu"

@__const.main.events = private unnamed_addr constant [6 x i32] [i32 1, i32 0, i32 1, i32 2, i32 0, i32 1], align 16

; Function Attrs: noinline nounwind uwtable
define dso_local i32 @step_fsm(i32 noundef %0, i32 noundef %1) #0 {
  %3 = alloca i32, align 4
  %4 = alloca i32, align 4
  %5 = alloca i32, align 4
  store i32 %0, ptr %4, align 4
  store i32 %1, ptr %5, align 4
  %6 = load i32, ptr %4, align 4
  switch i32 %6, label %31 [
    i32 0, label %7
    i32 1, label %12
    i32 2, label %25
    i32 3, label %30
    i32 4, label %30
  ]

7:                                                ; preds = %2
  %8 = load i32, ptr %5, align 4
  %9 = icmp eq i32 %8, 1
  %10 = zext i1 %9 to i64
  %11 = select i1 %9, i32 1, i32 0
  store i32 %11, ptr %3, align 4
  br label %32

12:                                               ; preds = %2
  %13 = load i32, ptr %5, align 4
  %14 = icmp eq i32 %13, 0
  br i1 %14, label %15, label %16

15:                                               ; preds = %12
  store i32 2, ptr %3, align 4
  br label %32

16:                                               ; preds = %12
  %17 = load i32, ptr %5, align 4
  %18 = icmp eq i32 %17, 2
  br i1 %18, label %19, label %20

19:                                               ; preds = %16
  store i32 3, ptr %3, align 4
  br label %32

20:                                               ; preds = %16
  %21 = load i32, ptr %5, align 4
  %22 = icmp eq i32 %21, 9
  br i1 %22, label %23, label %24

23:                                               ; preds = %20
  store i32 4, ptr %3, align 4
  br label %32

24:                                               ; preds = %20
  store i32 1, ptr %3, align 4
  br label %32

25:                                               ; preds = %2
  %26 = load i32, ptr %5, align 4
  %27 = icmp eq i32 %26, 1
  %28 = zext i1 %27 to i64
  %29 = select i1 %27, i32 1, i32 3
  store i32 %29, ptr %3, align 4
  br label %32

30:                                               ; preds = %2, %2
  br label %31

31:                                               ; preds = %2, %30
  store i32 0, ptr %3, align 4
  br label %32

32:                                               ; preds = %31, %25, %24, %23, %19, %15, %7
  %33 = load i32, ptr %3, align 4
  ret i32 %33
}

; Function Attrs: noinline nounwind uwtable
define dso_local i32 @main() #0 {
  %1 = alloca i32, align 4
  %2 = alloca i32, align 4
  %3 = alloca [6 x i32], align 16
  %4 = alloca i32, align 4
  store i32 0, ptr %1, align 4
  store i32 0, ptr %2, align 4
  call void @llvm.memcpy.p0.p0.i64(ptr align 16 %3, ptr align 16 @__const.main.events, i64 24, i1 false)
  store i32 0, ptr %4, align 4
  br label %5

5:                                                ; preds = %15, %0
  %6 = load i32, ptr %4, align 4
  %7 = icmp slt i32 %6, 6
  br i1 %7, label %8, label %18

8:                                                ; preds = %5
  %9 = load i32, ptr %2, align 4
  %10 = load i32, ptr %4, align 4
  %11 = sext i32 %10 to i64
  %12 = getelementptr inbounds [6 x i32], ptr %3, i64 0, i64 %11
  %13 = load i32, ptr %12, align 4
  %14 = call i32 @step_fsm(i32 noundef %9, i32 noundef %13)
  store i32 %14, ptr %2, align 4
  br label %15

15:                                               ; preds = %8
  %16 = load i32, ptr %4, align 4
  %17 = add nsw i32 %16, 1
  store i32 %17, ptr %4, align 4
  br label %5, !llvm.loop !7

18:                                               ; preds = %5
  %19 = load i32, ptr %2, align 4
  ret i32 %19
}

; Function Attrs: nocallback nofree nosync nounwind willreturn memory(argmem: readwrite)
declare void @llvm.memcpy.p0.p0.i64(ptr noalias writeonly captures(none), ptr noalias readonly captures(none), i64, i1 immarg) #1

attributes #0 = { noinline nounwind uwtable "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #1 = { nocallback nofree nosync nounwind willreturn memory(argmem: readwrite) }

!llvm.dbg.cu = !{!0}
!llvm.module.flags = !{!2, !3, !4, !5}
!llvm.ident = !{!6}

!0 = distinct !DICompileUnit(language: DW_LANG_C11, file: !1, producer: "clang version 23.1.2 (https://github.com/llvm/llvm-project 85ac560262434c9ccfc0c183ec22d4138ed647fb)", isOptimized: false, runtimeVersion: 0, emissionKind: NoDebug, splitDebugInlining: false, nameTableKind: None)
!1 = !DIFile(filename: "benchmarks/val\\PG033_state_machine.c", directory: "C:\\COMPILER PROJECT\\llvm-ml-pass-project")
!2 = !{i32 2, !"Debug Info Version", i32 3}
!3 = !{i32 8, !"PIC Level", i32 2}
!4 = !{i32 7, !"uwtable", i32 2}
!5 = !{i32 1, !"MaxTLSAlign", i32 65536}
!6 = !{!"clang version 23.1.2 (https://github.com/llvm/llvm-project 85ac560262434c9ccfc0c183ec22d4138ed647fb)"}
!7 = distinct !{!7, !8}
!8 = !{!"llvm.loop.mustprogress"}
