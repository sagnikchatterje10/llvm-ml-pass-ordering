; ModuleID = 'benchmarks\train\PG037_cellular_automata.c'
source_filename = "benchmarks\\train\\PG037_cellular_automata.c"
target datalayout = "e-m:w-p270:32:32-p271:32:32-p272:64:64-i64:64-i128:128-f80:128-n8:16:32:64-S128"
target triple = "x86_64-w64-windows-gnu"

; Function Attrs: noinline nounwind uwtable
define dso_local void @evolve_rule30(ptr noundef %0, i32 noundef %1) #0 {
  %3 = alloca ptr, align 8
  %4 = alloca i32, align 4
  %5 = alloca [32 x i8], align 16
  %6 = alloca i32, align 4
  %7 = alloca i32, align 4
  %8 = alloca i8, align 1
  %9 = alloca i8, align 1
  %10 = alloca i8, align 1
  %11 = alloca i32, align 4
  %12 = alloca i32, align 4
  store ptr %0, ptr %3, align 8
  store i32 %1, ptr %4, align 4
  store i32 0, ptr %6, align 4
  br label %13

13:                                               ; preds = %100, %2
  %14 = load i32, ptr %6, align 4
  %15 = load i32, ptr %4, align 4
  %16 = icmp slt i32 %14, %15
  br i1 %16, label %17, label %103

17:                                               ; preds = %13
  store i32 0, ptr %7, align 4
  br label %18

18:                                               ; preds = %80, %17
  %19 = load i32, ptr %7, align 4
  %20 = icmp slt i32 %19, 32
  br i1 %20, label %21, label %83

21:                                               ; preds = %18
  %22 = load i32, ptr %7, align 4
  %23 = icmp sgt i32 %22, 0
  br i1 %23, label %24, label %32

24:                                               ; preds = %21
  %25 = load ptr, ptr %3, align 8
  %26 = load i32, ptr %7, align 4
  %27 = sub nsw i32 %26, 1
  %28 = sext i32 %27 to i64
  %29 = getelementptr inbounds i8, ptr %25, i64 %28
  %30 = load i8, ptr %29, align 1
  %31 = zext i8 %30 to i32
  br label %37

32:                                               ; preds = %21
  %33 = load ptr, ptr %3, align 8
  %34 = getelementptr inbounds i8, ptr %33, i64 31
  %35 = load i8, ptr %34, align 1
  %36 = zext i8 %35 to i32
  br label %37

37:                                               ; preds = %32, %24
  %38 = phi i32 [ %31, %24 ], [ %36, %32 ]
  %39 = trunc i32 %38 to i8
  store i8 %39, ptr %8, align 1
  %40 = load ptr, ptr %3, align 8
  %41 = load i32, ptr %7, align 4
  %42 = sext i32 %41 to i64
  %43 = getelementptr inbounds i8, ptr %40, i64 %42
  %44 = load i8, ptr %43, align 1
  store i8 %44, ptr %9, align 1
  %45 = load i32, ptr %7, align 4
  %46 = icmp slt i32 %45, 31
  br i1 %46, label %47, label %55

47:                                               ; preds = %37
  %48 = load ptr, ptr %3, align 8
  %49 = load i32, ptr %7, align 4
  %50 = add nsw i32 %49, 1
  %51 = sext i32 %50 to i64
  %52 = getelementptr inbounds i8, ptr %48, i64 %51
  %53 = load i8, ptr %52, align 1
  %54 = zext i8 %53 to i32
  br label %60

55:                                               ; preds = %37
  %56 = load ptr, ptr %3, align 8
  %57 = getelementptr inbounds i8, ptr %56, i64 0
  %58 = load i8, ptr %57, align 1
  %59 = zext i8 %58 to i32
  br label %60

60:                                               ; preds = %55, %47
  %61 = phi i32 [ %54, %47 ], [ %59, %55 ]
  %62 = trunc i32 %61 to i8
  store i8 %62, ptr %10, align 1
  %63 = load i8, ptr %8, align 1
  %64 = zext i8 %63 to i32
  %65 = shl i32 %64, 2
  %66 = load i8, ptr %9, align 1
  %67 = zext i8 %66 to i32
  %68 = shl i32 %67, 1
  %69 = or i32 %65, %68
  %70 = load i8, ptr %10, align 1
  %71 = zext i8 %70 to i32
  %72 = or i32 %69, %71
  store i32 %72, ptr %11, align 4
  %73 = load i32, ptr %11, align 4
  %74 = ashr i32 30, %73
  %75 = and i32 %74, 1
  %76 = trunc i32 %75 to i8
  %77 = load i32, ptr %7, align 4
  %78 = sext i32 %77 to i64
  %79 = getelementptr inbounds [32 x i8], ptr %5, i64 0, i64 %78
  store i8 %76, ptr %79, align 1
  br label %80

80:                                               ; preds = %60
  %81 = load i32, ptr %7, align 4
  %82 = add nsw i32 %81, 1
  store i32 %82, ptr %7, align 4
  br label %18, !llvm.loop !7

83:                                               ; preds = %18
  store i32 0, ptr %12, align 4
  br label %84

84:                                               ; preds = %96, %83
  %85 = load i32, ptr %12, align 4
  %86 = icmp slt i32 %85, 32
  br i1 %86, label %87, label %99

87:                                               ; preds = %84
  %88 = load i32, ptr %12, align 4
  %89 = sext i32 %88 to i64
  %90 = getelementptr inbounds [32 x i8], ptr %5, i64 0, i64 %89
  %91 = load i8, ptr %90, align 1
  %92 = load ptr, ptr %3, align 8
  %93 = load i32, ptr %12, align 4
  %94 = sext i32 %93 to i64
  %95 = getelementptr inbounds i8, ptr %92, i64 %94
  store i8 %91, ptr %95, align 1
  br label %96

96:                                               ; preds = %87
  %97 = load i32, ptr %12, align 4
  %98 = add nsw i32 %97, 1
  store i32 %98, ptr %12, align 4
  br label %84, !llvm.loop !9

99:                                               ; preds = %84
  br label %100

100:                                              ; preds = %99
  %101 = load i32, ptr %6, align 4
  %102 = add nsw i32 %101, 1
  store i32 %102, ptr %6, align 4
  br label %13, !llvm.loop !10

103:                                              ; preds = %13
  ret void
}

; Function Attrs: noinline nounwind uwtable
define dso_local i32 @main() #0 {
  %1 = alloca i32, align 4
  %2 = alloca [32 x i8], align 16
  %3 = alloca i32, align 4
  %4 = alloca i32, align 4
  store i32 0, ptr %1, align 4
  call void @llvm.memset.p0.i64(ptr align 16 %2, i8 0, i64 32, i1 false)
  %5 = getelementptr inbounds [32 x i8], ptr %2, i64 0, i64 16
  store i8 1, ptr %5, align 16
  %6 = getelementptr inbounds [32 x i8], ptr %2, i64 0, i64 0
  call void @evolve_rule30(ptr noundef %6, i32 noundef 10)
  store i32 0, ptr %3, align 4
  store i32 0, ptr %4, align 4
  br label %7

7:                                                ; preds = %18, %0
  %8 = load i32, ptr %4, align 4
  %9 = icmp slt i32 %8, 32
  br i1 %9, label %10, label %21

10:                                               ; preds = %7
  %11 = load i32, ptr %4, align 4
  %12 = sext i32 %11 to i64
  %13 = getelementptr inbounds [32 x i8], ptr %2, i64 0, i64 %12
  %14 = load i8, ptr %13, align 1
  %15 = zext i8 %14 to i32
  %16 = load i32, ptr %3, align 4
  %17 = add nsw i32 %16, %15
  store i32 %17, ptr %3, align 4
  br label %18

18:                                               ; preds = %10
  %19 = load i32, ptr %4, align 4
  %20 = add nsw i32 %19, 1
  store i32 %20, ptr %4, align 4
  br label %7, !llvm.loop !11

21:                                               ; preds = %7
  %22 = load i32, ptr %3, align 4
  ret i32 %22
}

; Function Attrs: nocallback nofree nosync nounwind willreturn memory(argmem: write)
declare void @llvm.memset.p0.i64(ptr writeonly captures(none), i8, i64, i1 immarg) #1

attributes #0 = { noinline nounwind uwtable "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #1 = { nocallback nofree nosync nounwind willreturn memory(argmem: write) }

!llvm.dbg.cu = !{!0}
!llvm.module.flags = !{!2, !3, !4, !5}
!llvm.ident = !{!6}

!0 = distinct !DICompileUnit(language: DW_LANG_C11, file: !1, producer: "clang version 23.1.2 (https://github.com/llvm/llvm-project 85ac560262434c9ccfc0c183ec22d4138ed647fb)", isOptimized: false, runtimeVersion: 0, emissionKind: NoDebug, splitDebugInlining: false, nameTableKind: None)
!1 = !DIFile(filename: "benchmarks\\train\\PG037_cellular_automata.c", directory: "C:\\COMPILER PROJECT\\llvm-ml-pass-project")
!2 = !{i32 2, !"Debug Info Version", i32 3}
!3 = !{i32 8, !"PIC Level", i32 2}
!4 = !{i32 7, !"uwtable", i32 2}
!5 = !{i32 1, !"MaxTLSAlign", i32 65536}
!6 = !{!"clang version 23.1.2 (https://github.com/llvm/llvm-project 85ac560262434c9ccfc0c183ec22d4138ed647fb)"}
!7 = distinct !{!7, !8}
!8 = !{!"llvm.loop.mustprogress"}
!9 = distinct !{!9, !8}
!10 = distinct !{!10, !8}
!11 = distinct !{!11, !8}
