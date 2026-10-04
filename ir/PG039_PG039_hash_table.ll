; ModuleID = 'benchmarks/train/PG039_hash_table.c'
source_filename = "benchmarks/train/PG039_hash_table.c"
target datalayout = "e-m:w-p270:32:32-p271:32:32-p272:64:64-i64:64-i128:128-f80:128-n8:16:32:64-S128"
target triple = "x86_64-w64-windows-gnu"

%struct.HashEntry = type { i32, i32, i32 }

; Function Attrs: noinline nounwind uwtable
define dso_local void @ht_init(ptr noundef %0) #0 {
  %2 = alloca ptr, align 8
  %3 = alloca i32, align 4
  store ptr %0, ptr %2, align 8
  store i32 0, ptr %3, align 4
  br label %4

4:                                                ; preds = %13, %1
  %5 = load i32, ptr %3, align 4
  %6 = icmp slt i32 %5, 16
  br i1 %6, label %7, label %16

7:                                                ; preds = %4
  %8 = load ptr, ptr %2, align 8
  %9 = load i32, ptr %3, align 4
  %10 = sext i32 %9 to i64
  %11 = getelementptr inbounds %struct.HashEntry, ptr %8, i64 %10
  %12 = getelementptr inbounds nuw %struct.HashEntry, ptr %11, i32 0, i32 2
  store i32 0, ptr %12, align 4
  br label %13

13:                                               ; preds = %7
  %14 = load i32, ptr %3, align 4
  %15 = add nsw i32 %14, 1
  store i32 %15, ptr %3, align 4
  br label %4, !llvm.loop !7

16:                                               ; preds = %4
  ret void
}

; Function Attrs: noinline nounwind uwtable
define dso_local void @ht_insert(ptr noundef %0, i32 noundef %1, i32 noundef %2) #0 {
  %4 = alloca ptr, align 8
  %5 = alloca i32, align 4
  %6 = alloca i32, align 4
  %7 = alloca i32, align 4
  %8 = alloca i32, align 4
  %9 = alloca i32, align 4
  store ptr %0, ptr %4, align 8
  store i32 %1, ptr %5, align 4
  store i32 %2, ptr %6, align 4
  %10 = load i32, ptr %5, align 4
  %11 = icmp sge i32 %10, 0
  br i1 %11, label %12, label %14

12:                                               ; preds = %3
  %13 = load i32, ptr %5, align 4
  br label %17

14:                                               ; preds = %3
  %15 = load i32, ptr %5, align 4
  %16 = sub nsw i32 0, %15
  br label %17

17:                                               ; preds = %14, %12
  %18 = phi i32 [ %13, %12 ], [ %16, %14 ]
  %19 = srem i32 %18, 16
  store i32 %19, ptr %7, align 4
  store i32 0, ptr %8, align 4
  br label %20

20:                                               ; preds = %63, %17
  %21 = load i32, ptr %8, align 4
  %22 = icmp slt i32 %21, 16
  br i1 %22, label %23, label %66

23:                                               ; preds = %20
  %24 = load i32, ptr %7, align 4
  %25 = load i32, ptr %8, align 4
  %26 = add nsw i32 %24, %25
  %27 = srem i32 %26, 16
  store i32 %27, ptr %9, align 4
  %28 = load ptr, ptr %4, align 8
  %29 = load i32, ptr %9, align 4
  %30 = sext i32 %29 to i64
  %31 = getelementptr inbounds %struct.HashEntry, ptr %28, i64 %30
  %32 = getelementptr inbounds nuw %struct.HashEntry, ptr %31, i32 0, i32 2
  %33 = load i32, ptr %32, align 4
  %34 = icmp ne i32 %33, 0
  br i1 %34, label %35, label %44

35:                                               ; preds = %23
  %36 = load ptr, ptr %4, align 8
  %37 = load i32, ptr %9, align 4
  %38 = sext i32 %37 to i64
  %39 = getelementptr inbounds %struct.HashEntry, ptr %36, i64 %38
  %40 = getelementptr inbounds nuw %struct.HashEntry, ptr %39, i32 0, i32 0
  %41 = load i32, ptr %40, align 4
  %42 = load i32, ptr %5, align 4
  %43 = icmp eq i32 %41, %42
  br i1 %43, label %44, label %62

44:                                               ; preds = %35, %23
  %45 = load i32, ptr %5, align 4
  %46 = load ptr, ptr %4, align 8
  %47 = load i32, ptr %9, align 4
  %48 = sext i32 %47 to i64
  %49 = getelementptr inbounds %struct.HashEntry, ptr %46, i64 %48
  %50 = getelementptr inbounds nuw %struct.HashEntry, ptr %49, i32 0, i32 0
  store i32 %45, ptr %50, align 4
  %51 = load i32, ptr %6, align 4
  %52 = load ptr, ptr %4, align 8
  %53 = load i32, ptr %9, align 4
  %54 = sext i32 %53 to i64
  %55 = getelementptr inbounds %struct.HashEntry, ptr %52, i64 %54
  %56 = getelementptr inbounds nuw %struct.HashEntry, ptr %55, i32 0, i32 1
  store i32 %51, ptr %56, align 4
  %57 = load ptr, ptr %4, align 8
  %58 = load i32, ptr %9, align 4
  %59 = sext i32 %58 to i64
  %60 = getelementptr inbounds %struct.HashEntry, ptr %57, i64 %59
  %61 = getelementptr inbounds nuw %struct.HashEntry, ptr %60, i32 0, i32 2
  store i32 1, ptr %61, align 4
  br label %66

62:                                               ; preds = %35
  br label %63

63:                                               ; preds = %62
  %64 = load i32, ptr %8, align 4
  %65 = add nsw i32 %64, 1
  store i32 %65, ptr %8, align 4
  br label %20, !llvm.loop !9

66:                                               ; preds = %44, %20
  ret void
}

; Function Attrs: noinline nounwind uwtable
define dso_local i32 @ht_lookup(ptr noundef %0, i32 noundef %1) #0 {
  %3 = alloca i32, align 4
  %4 = alloca ptr, align 8
  %5 = alloca i32, align 4
  %6 = alloca i32, align 4
  %7 = alloca i32, align 4
  %8 = alloca i32, align 4
  store ptr %0, ptr %4, align 8
  store i32 %1, ptr %5, align 4
  %9 = load i32, ptr %5, align 4
  %10 = icmp sge i32 %9, 0
  br i1 %10, label %11, label %13

11:                                               ; preds = %2
  %12 = load i32, ptr %5, align 4
  br label %16

13:                                               ; preds = %2
  %14 = load i32, ptr %5, align 4
  %15 = sub nsw i32 0, %14
  br label %16

16:                                               ; preds = %13, %11
  %17 = phi i32 [ %12, %11 ], [ %15, %13 ]
  %18 = srem i32 %17, 16
  store i32 %18, ptr %6, align 4
  store i32 0, ptr %7, align 4
  br label %19

19:                                               ; preds = %52, %16
  %20 = load i32, ptr %7, align 4
  %21 = icmp slt i32 %20, 16
  br i1 %21, label %22, label %55

22:                                               ; preds = %19
  %23 = load i32, ptr %6, align 4
  %24 = load i32, ptr %7, align 4
  %25 = add nsw i32 %23, %24
  %26 = srem i32 %25, 16
  store i32 %26, ptr %8, align 4
  %27 = load ptr, ptr %4, align 8
  %28 = load i32, ptr %8, align 4
  %29 = sext i32 %28 to i64
  %30 = getelementptr inbounds %struct.HashEntry, ptr %27, i64 %29
  %31 = getelementptr inbounds nuw %struct.HashEntry, ptr %30, i32 0, i32 2
  %32 = load i32, ptr %31, align 4
  %33 = icmp ne i32 %32, 0
  br i1 %33, label %35, label %34

34:                                               ; preds = %22
  store i32 -1, ptr %3, align 4
  br label %56

35:                                               ; preds = %22
  %36 = load ptr, ptr %4, align 8
  %37 = load i32, ptr %8, align 4
  %38 = sext i32 %37 to i64
  %39 = getelementptr inbounds %struct.HashEntry, ptr %36, i64 %38
  %40 = getelementptr inbounds nuw %struct.HashEntry, ptr %39, i32 0, i32 0
  %41 = load i32, ptr %40, align 4
  %42 = load i32, ptr %5, align 4
  %43 = icmp eq i32 %41, %42
  br i1 %43, label %44, label %51

44:                                               ; preds = %35
  %45 = load ptr, ptr %4, align 8
  %46 = load i32, ptr %8, align 4
  %47 = sext i32 %46 to i64
  %48 = getelementptr inbounds %struct.HashEntry, ptr %45, i64 %47
  %49 = getelementptr inbounds nuw %struct.HashEntry, ptr %48, i32 0, i32 1
  %50 = load i32, ptr %49, align 4
  store i32 %50, ptr %3, align 4
  br label %56

51:                                               ; preds = %35
  br label %52

52:                                               ; preds = %51
  %53 = load i32, ptr %7, align 4
  %54 = add nsw i32 %53, 1
  store i32 %54, ptr %7, align 4
  br label %19, !llvm.loop !10

55:                                               ; preds = %19
  store i32 -1, ptr %3, align 4
  br label %56

56:                                               ; preds = %55, %44, %34
  %57 = load i32, ptr %3, align 4
  ret i32 %57
}

; Function Attrs: noinline nounwind uwtable
define dso_local i32 @main() #0 {
  %1 = alloca i32, align 4
  %2 = alloca [16 x %struct.HashEntry], align 16
  %3 = alloca i32, align 4
  %4 = alloca i32, align 4
  store i32 0, ptr %1, align 4
  %5 = getelementptr inbounds [16 x %struct.HashEntry], ptr %2, i64 0, i64 0
  call void @ht_init(ptr noundef %5)
  %6 = getelementptr inbounds [16 x %struct.HashEntry], ptr %2, i64 0, i64 0
  call void @ht_insert(ptr noundef %6, i32 noundef 101, i32 noundef 500)
  %7 = getelementptr inbounds [16 x %struct.HashEntry], ptr %2, i64 0, i64 0
  call void @ht_insert(ptr noundef %7, i32 noundef 117, i32 noundef 600)
  %8 = getelementptr inbounds [16 x %struct.HashEntry], ptr %2, i64 0, i64 0
  call void @ht_insert(ptr noundef %8, i32 noundef 202, i32 noundef 700)
  %9 = getelementptr inbounds [16 x %struct.HashEntry], ptr %2, i64 0, i64 0
  %10 = call i32 @ht_lookup(ptr noundef %9, i32 noundef 101)
  store i32 %10, ptr %3, align 4
  %11 = getelementptr inbounds [16 x %struct.HashEntry], ptr %2, i64 0, i64 0
  %12 = call i32 @ht_lookup(ptr noundef %11, i32 noundef 117)
  store i32 %12, ptr %4, align 4
  %13 = load i32, ptr %3, align 4
  %14 = load i32, ptr %4, align 4
  %15 = add nsw i32 %13, %14
  %16 = and i32 %15, 255
  ret i32 %16
}

attributes #0 = { noinline nounwind uwtable "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }

!llvm.dbg.cu = !{!0}
!llvm.module.flags = !{!2, !3, !4, !5}
!llvm.ident = !{!6}

!0 = distinct !DICompileUnit(language: DW_LANG_C11, file: !1, producer: "clang version 23.1.2 (https://github.com/llvm/llvm-project 85ac560262434c9ccfc0c183ec22d4138ed647fb)", isOptimized: false, runtimeVersion: 0, emissionKind: NoDebug, splitDebugInlining: false, nameTableKind: None)
!1 = !DIFile(filename: "benchmarks/train\\PG039_hash_table.c", directory: "C:\\COMPILER PROJECT\\llvm-ml-pass-project")
!2 = !{i32 2, !"Debug Info Version", i32 3}
!3 = !{i32 8, !"PIC Level", i32 2}
!4 = !{i32 7, !"uwtable", i32 2}
!5 = !{i32 1, !"MaxTLSAlign", i32 65536}
!6 = !{!"clang version 23.1.2 (https://github.com/llvm/llvm-project 85ac560262434c9ccfc0c183ec22d4138ed647fb)"}
!7 = distinct !{!7, !8}
!8 = !{!"llvm.loop.mustprogress"}
!9 = distinct !{!9, !8}
!10 = distinct !{!10, !8}
