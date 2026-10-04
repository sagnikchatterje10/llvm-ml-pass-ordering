; ModuleID = 'benchmarks\test\PG040_knapsack.c'
source_filename = "benchmarks\\test\\PG040_knapsack.c"
target datalayout = "e-m:w-p270:32:32-p271:32:32-p272:64:64-i64:64-i128:128-f80:128-n8:16:32:64-S128"
target triple = "x86_64-w64-windows-gnu"

@__const.main.val = private unnamed_addr constant [4 x i32] [i32 60, i32 100, i32 120, i32 80], align 16
@__const.main.wt = private unnamed_addr constant [4 x i32] [i32 10, i32 20, i32 30, i32 15], align 16

; Function Attrs: noinline nounwind uwtable
define dso_local i32 @knapsack(i32 noundef %0, ptr noundef %1, ptr noundef %2, i32 noundef %3) #0 {
  %5 = alloca i32, align 4
  %6 = alloca ptr, align 8
  %7 = alloca ptr, align 8
  %8 = alloca i32, align 4
  %9 = alloca [16 x [32 x i32]], align 16
  %10 = alloca i32, align 4
  %11 = alloca i32, align 4
  store i32 %0, ptr %5, align 4
  store ptr %1, ptr %6, align 8
  store ptr %2, ptr %7, align 8
  store i32 %3, ptr %8, align 4
  call void @llvm.memset.p0.i64(ptr align 16 %9, i8 0, i64 2048, i1 false)
  store i32 1, ptr %10, align 4
  br label %12

12:                                               ; preds = %122, %4
  %13 = load i32, ptr %10, align 4
  %14 = load i32, ptr %8, align 4
  %15 = icmp sle i32 %13, %14
  br i1 %15, label %16, label %125

16:                                               ; preds = %12
  store i32 1, ptr %11, align 4
  br label %17

17:                                               ; preds = %118, %16
  %18 = load i32, ptr %11, align 4
  %19 = load i32, ptr %5, align 4
  %20 = icmp sle i32 %18, %19
  br i1 %20, label %21, label %121

21:                                               ; preds = %17
  %22 = load ptr, ptr %6, align 8
  %23 = load i32, ptr %10, align 4
  %24 = sub nsw i32 %23, 1
  %25 = sext i32 %24 to i64
  %26 = getelementptr inbounds i32, ptr %22, i64 %25
  %27 = load i32, ptr %26, align 4
  %28 = load i32, ptr %11, align 4
  %29 = icmp sle i32 %27, %28
  br i1 %29, label %30, label %102

30:                                               ; preds = %21
  %31 = load ptr, ptr %7, align 8
  %32 = load i32, ptr %10, align 4
  %33 = sub nsw i32 %32, 1
  %34 = sext i32 %33 to i64
  %35 = getelementptr inbounds i32, ptr %31, i64 %34
  %36 = load i32, ptr %35, align 4
  %37 = load i32, ptr %10, align 4
  %38 = sub nsw i32 %37, 1
  %39 = sext i32 %38 to i64
  %40 = getelementptr inbounds [16 x [32 x i32]], ptr %9, i64 0, i64 %39
  %41 = load i32, ptr %11, align 4
  %42 = load ptr, ptr %6, align 8
  %43 = load i32, ptr %10, align 4
  %44 = sub nsw i32 %43, 1
  %45 = sext i32 %44 to i64
  %46 = getelementptr inbounds i32, ptr %42, i64 %45
  %47 = load i32, ptr %46, align 4
  %48 = sub nsw i32 %41, %47
  %49 = sext i32 %48 to i64
  %50 = getelementptr inbounds [32 x i32], ptr %40, i64 0, i64 %49
  %51 = load i32, ptr %50, align 4
  %52 = add nsw i32 %36, %51
  %53 = load i32, ptr %10, align 4
  %54 = sub nsw i32 %53, 1
  %55 = sext i32 %54 to i64
  %56 = getelementptr inbounds [16 x [32 x i32]], ptr %9, i64 0, i64 %55
  %57 = load i32, ptr %11, align 4
  %58 = sext i32 %57 to i64
  %59 = getelementptr inbounds [32 x i32], ptr %56, i64 0, i64 %58
  %60 = load i32, ptr %59, align 4
  %61 = icmp sgt i32 %52, %60
  br i1 %61, label %62, label %85

62:                                               ; preds = %30
  %63 = load ptr, ptr %7, align 8
  %64 = load i32, ptr %10, align 4
  %65 = sub nsw i32 %64, 1
  %66 = sext i32 %65 to i64
  %67 = getelementptr inbounds i32, ptr %63, i64 %66
  %68 = load i32, ptr %67, align 4
  %69 = load i32, ptr %10, align 4
  %70 = sub nsw i32 %69, 1
  %71 = sext i32 %70 to i64
  %72 = getelementptr inbounds [16 x [32 x i32]], ptr %9, i64 0, i64 %71
  %73 = load i32, ptr %11, align 4
  %74 = load ptr, ptr %6, align 8
  %75 = load i32, ptr %10, align 4
  %76 = sub nsw i32 %75, 1
  %77 = sext i32 %76 to i64
  %78 = getelementptr inbounds i32, ptr %74, i64 %77
  %79 = load i32, ptr %78, align 4
  %80 = sub nsw i32 %73, %79
  %81 = sext i32 %80 to i64
  %82 = getelementptr inbounds [32 x i32], ptr %72, i64 0, i64 %81
  %83 = load i32, ptr %82, align 4
  %84 = add nsw i32 %68, %83
  br label %94

85:                                               ; preds = %30
  %86 = load i32, ptr %10, align 4
  %87 = sub nsw i32 %86, 1
  %88 = sext i32 %87 to i64
  %89 = getelementptr inbounds [16 x [32 x i32]], ptr %9, i64 0, i64 %88
  %90 = load i32, ptr %11, align 4
  %91 = sext i32 %90 to i64
  %92 = getelementptr inbounds [32 x i32], ptr %89, i64 0, i64 %91
  %93 = load i32, ptr %92, align 4
  br label %94

94:                                               ; preds = %85, %62
  %95 = phi i32 [ %84, %62 ], [ %93, %85 ]
  %96 = load i32, ptr %10, align 4
  %97 = sext i32 %96 to i64
  %98 = getelementptr inbounds [16 x [32 x i32]], ptr %9, i64 0, i64 %97
  %99 = load i32, ptr %11, align 4
  %100 = sext i32 %99 to i64
  %101 = getelementptr inbounds [32 x i32], ptr %98, i64 0, i64 %100
  store i32 %95, ptr %101, align 4
  br label %117

102:                                              ; preds = %21
  %103 = load i32, ptr %10, align 4
  %104 = sub nsw i32 %103, 1
  %105 = sext i32 %104 to i64
  %106 = getelementptr inbounds [16 x [32 x i32]], ptr %9, i64 0, i64 %105
  %107 = load i32, ptr %11, align 4
  %108 = sext i32 %107 to i64
  %109 = getelementptr inbounds [32 x i32], ptr %106, i64 0, i64 %108
  %110 = load i32, ptr %109, align 4
  %111 = load i32, ptr %10, align 4
  %112 = sext i32 %111 to i64
  %113 = getelementptr inbounds [16 x [32 x i32]], ptr %9, i64 0, i64 %112
  %114 = load i32, ptr %11, align 4
  %115 = sext i32 %114 to i64
  %116 = getelementptr inbounds [32 x i32], ptr %113, i64 0, i64 %115
  store i32 %110, ptr %116, align 4
  br label %117

117:                                              ; preds = %102, %94
  br label %118

118:                                              ; preds = %117
  %119 = load i32, ptr %11, align 4
  %120 = add nsw i32 %119, 1
  store i32 %120, ptr %11, align 4
  br label %17, !llvm.loop !7

121:                                              ; preds = %17
  br label %122

122:                                              ; preds = %121
  %123 = load i32, ptr %10, align 4
  %124 = add nsw i32 %123, 1
  store i32 %124, ptr %10, align 4
  br label %12, !llvm.loop !9

125:                                              ; preds = %12
  %126 = load i32, ptr %8, align 4
  %127 = sext i32 %126 to i64
  %128 = getelementptr inbounds [16 x [32 x i32]], ptr %9, i64 0, i64 %127
  %129 = load i32, ptr %5, align 4
  %130 = sext i32 %129 to i64
  %131 = getelementptr inbounds [32 x i32], ptr %128, i64 0, i64 %130
  %132 = load i32, ptr %131, align 4
  ret i32 %132
}

; Function Attrs: nocallback nofree nosync nounwind willreturn memory(argmem: write)
declare void @llvm.memset.p0.i64(ptr writeonly captures(none), i8, i64, i1 immarg) #1

; Function Attrs: noinline nounwind uwtable
define dso_local i32 @main() #0 {
  %1 = alloca i32, align 4
  %2 = alloca [4 x i32], align 16
  %3 = alloca [4 x i32], align 16
  %4 = alloca i32, align 4
  %5 = alloca i32, align 4
  store i32 0, ptr %1, align 4
  call void @llvm.memcpy.p0.p0.i64(ptr align 16 %2, ptr align 16 @__const.main.val, i64 16, i1 false)
  call void @llvm.memcpy.p0.p0.i64(ptr align 16 %3, ptr align 16 @__const.main.wt, i64 16, i1 false)
  store i32 30, ptr %4, align 4
  %6 = load i32, ptr %4, align 4
  %7 = getelementptr inbounds [4 x i32], ptr %3, i64 0, i64 0
  %8 = getelementptr inbounds [4 x i32], ptr %2, i64 0, i64 0
  %9 = call i32 @knapsack(i32 noundef %6, ptr noundef %7, ptr noundef %8, i32 noundef 4)
  store i32 %9, ptr %5, align 4
  %10 = load i32, ptr %5, align 4
  %11 = and i32 %10, 255
  ret i32 %11
}

; Function Attrs: nocallback nofree nosync nounwind willreturn memory(argmem: readwrite)
declare void @llvm.memcpy.p0.p0.i64(ptr noalias writeonly captures(none), ptr noalias readonly captures(none), i64, i1 immarg) #2

attributes #0 = { noinline nounwind uwtable "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #1 = { nocallback nofree nosync nounwind willreturn memory(argmem: write) }
attributes #2 = { nocallback nofree nosync nounwind willreturn memory(argmem: readwrite) }

!llvm.dbg.cu = !{!0}
!llvm.module.flags = !{!2, !3, !4, !5}
!llvm.ident = !{!6}

!0 = distinct !DICompileUnit(language: DW_LANG_C11, file: !1, producer: "clang version 23.1.2 (https://github.com/llvm/llvm-project 85ac560262434c9ccfc0c183ec22d4138ed647fb)", isOptimized: false, runtimeVersion: 0, emissionKind: NoDebug, splitDebugInlining: false, nameTableKind: None)
!1 = !DIFile(filename: "benchmarks\\test\\PG040_knapsack.c", directory: "C:\\COMPILER PROJECT\\llvm-ml-pass-project")
!2 = !{i32 2, !"Debug Info Version", i32 3}
!3 = !{i32 8, !"PIC Level", i32 2}
!4 = !{i32 7, !"uwtable", i32 2}
!5 = !{i32 1, !"MaxTLSAlign", i32 65536}
!6 = !{!"clang version 23.1.2 (https://github.com/llvm/llvm-project 85ac560262434c9ccfc0c183ec22d4138ed647fb)"}
!7 = distinct !{!7, !8}
!8 = !{!"llvm.loop.mustprogress"}
!9 = distinct !{!9, !8}
