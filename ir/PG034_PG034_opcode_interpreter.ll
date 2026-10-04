; ModuleID = 'benchmarks/val/PG034_opcode_interpreter.c'
source_filename = "benchmarks/val/PG034_opcode_interpreter.c"
target datalayout = "e-m:w-p270:32:32-p271:32:32-p272:64:64-i64:64-i128:128-f80:128-n8:16:32:64-S128"
target triple = "x86_64-w64-windows-gnu"

@__const.main.program = private unnamed_addr constant [10 x i32] [i32 1, i32 15, i32 3, i32 3, i32 2, i32 5, i32 4, i32 0, i32 1, i32 99], align 16

; Function Attrs: noinline nounwind uwtable
define dso_local i32 @run_vm(ptr noundef %0, i32 noundef %1) #0 {
  %3 = alloca i32, align 4
  %4 = alloca ptr, align 8
  %5 = alloca i32, align 4
  %6 = alloca i32, align 4
  %7 = alloca i32, align 4
  %8 = alloca i32, align 4
  %9 = alloca i32, align 4
  store ptr %0, ptr %4, align 8
  store i32 %1, ptr %5, align 4
  store i32 0, ptr %6, align 4
  store i32 0, ptr %7, align 4
  br label %10

10:                                               ; preds = %45, %2
  %11 = load i32, ptr %7, align 4
  %12 = load i32, ptr %5, align 4
  %13 = icmp slt i32 %11, %12
  br i1 %13, label %14, label %48

14:                                               ; preds = %10
  %15 = load ptr, ptr %4, align 8
  %16 = load i32, ptr %7, align 4
  %17 = sext i32 %16 to i64
  %18 = getelementptr inbounds i32, ptr %15, i64 %17
  %19 = load i32, ptr %18, align 4
  store i32 %19, ptr %8, align 4
  %20 = load ptr, ptr %4, align 8
  %21 = load i32, ptr %7, align 4
  %22 = add nsw i32 %21, 1
  %23 = sext i32 %22 to i64
  %24 = getelementptr inbounds i32, ptr %20, i64 %23
  %25 = load i32, ptr %24, align 4
  store i32 %25, ptr %9, align 4
  %26 = load i32, ptr %8, align 4
  switch i32 %26, label %42 [
    i32 0, label %27
    i32 1, label %28
    i32 2, label %32
    i32 3, label %36
    i32 4, label %40
  ]

27:                                               ; preds = %14
  br label %44

28:                                               ; preds = %14
  %29 = load i32, ptr %9, align 4
  %30 = load i32, ptr %6, align 4
  %31 = add nsw i32 %30, %29
  store i32 %31, ptr %6, align 4
  br label %44

32:                                               ; preds = %14
  %33 = load i32, ptr %9, align 4
  %34 = load i32, ptr %6, align 4
  %35 = sub nsw i32 %34, %33
  store i32 %35, ptr %6, align 4
  br label %44

36:                                               ; preds = %14
  %37 = load i32, ptr %9, align 4
  %38 = load i32, ptr %6, align 4
  %39 = mul nsw i32 %38, %37
  store i32 %39, ptr %6, align 4
  br label %44

40:                                               ; preds = %14
  %41 = load i32, ptr %6, align 4
  store i32 %41, ptr %3, align 4
  br label %50

42:                                               ; preds = %14
  store i32 -1, ptr %6, align 4
  %43 = load i32, ptr %6, align 4
  store i32 %43, ptr %3, align 4
  br label %50

44:                                               ; preds = %36, %32, %28, %27
  br label %45

45:                                               ; preds = %44
  %46 = load i32, ptr %7, align 4
  %47 = add nsw i32 %46, 2
  store i32 %47, ptr %7, align 4
  br label %10, !llvm.loop !7

48:                                               ; preds = %10
  %49 = load i32, ptr %6, align 4
  store i32 %49, ptr %3, align 4
  br label %50

50:                                               ; preds = %48, %42, %40
  %51 = load i32, ptr %3, align 4
  ret i32 %51
}

; Function Attrs: noinline nounwind uwtable
define dso_local i32 @main() #0 {
  %1 = alloca i32, align 4
  %2 = alloca [10 x i32], align 16
  %3 = alloca i32, align 4
  store i32 0, ptr %1, align 4
  call void @llvm.memcpy.p0.p0.i64(ptr align 16 %2, ptr align 16 @__const.main.program, i64 40, i1 false)
  %4 = getelementptr inbounds [10 x i32], ptr %2, i64 0, i64 0
  %5 = call i32 @run_vm(ptr noundef %4, i32 noundef 10)
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
!1 = !DIFile(filename: "benchmarks/val\\PG034_opcode_interpreter.c", directory: "C:\\COMPILER PROJECT\\llvm-ml-pass-project")
!2 = !{i32 2, !"Debug Info Version", i32 3}
!3 = !{i32 8, !"PIC Level", i32 2}
!4 = !{i32 7, !"uwtable", i32 2}
!5 = !{i32 1, !"MaxTLSAlign", i32 65536}
!6 = !{!"clang version 23.1.2 (https://github.com/llvm/llvm-project 85ac560262434c9ccfc0c183ec22d4138ed647fb)"}
!7 = distinct !{!7, !8}
!8 = !{!"llvm.loop.mustprogress"}
