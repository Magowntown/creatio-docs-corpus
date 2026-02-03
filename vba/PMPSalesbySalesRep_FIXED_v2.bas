Option Explicit
Dim iFila As Long
Dim sHoja As String

Dim dTotCType As Double
Dim dTotCustomer As Double

Dim dGranTotal As Double

Sub PMPMain()
    '
    ' PMPSalesbySalesBySalesRep Macro
    '
    Application.ScreenUpdating = False
    Application.Calculation = xlCalculationManual

    Call PMPInicializo
    Call PMPCabezalListado
    Call PMPOrdenoCrudo
    Call Formato_americano
    Call PMPFillReportData

    Application.Calculation = xlCalculationAutomatic
    Application.ScreenUpdating = True
iFila = 0
End Sub

Sub PMPInicializo()
    ' inicializo la hoja de salida del reporte
    Worksheets("Rpt").Select
    Columns("A:I").Select
    Selection.Delete Shift:=xlToLeft
    ActiveWindow.FreezePanes = False
    Range("A1").Select

    Cells.Select
    With Selection.Interior
        .PatternColorIndex = xlAutomatic
        .ThemeColor = xlThemeColorDark1
        .TintAndShade = 0
        .PatternTintAndShade = 0
    End With
End Sub


Sub PMPCabezalListado()

    Dim sFecStart As String
    Dim sAuxFecStart As String
    Dim sFecEnd As String
    Dim sAuxFecEnd As String
    Dim iSpace As Integer

    Worksheets("Rpt").Select

    Range("A:C").Select
    With Selection
        .HorizontalAlignment = xlLeft
    End With

    Range("A1:G1").Select
    With Selection
        .HorizontalAlignment = xlCenter
        .VerticalAlignment = xlBottom
        .WrapText = False
        .Orientation = 0
        .AddIndent = False
        .IndentLevel = 0
        .ShrinkToFit = False
        .ReadingOrder = xlLTR
        .MergeCells = False
    End With
    Selection.Merge
    Range("A1:G1").Select
    With Selection.Font
        .Name = "Arial"
        .Size = 12
        .Strikethrough = False
        .Superscript = False
        .Subscript = False
        .OutlineFont = False
        .Shadow = False
        .Underline = xlUnderlineStyleNone
        .Color = -16777216
        .TintAndShade = 0
        .ThemeFont = xlThemeFontNone
    End With
    Selection.Font.Bold = True
    ActiveCell.FormulaR1C1 = "Sales by Item By Type Of Customer"

    Range("A2:G2").Select
    With Selection
        .HorizontalAlignment = xlCenter
        .VerticalAlignment = xlBottom
        .WrapText = False
        .Orientation = 0
        .AddIndent = False
        .IndentLevel = 0
        .ShrinkToFit = False
        .ReadingOrder = xlLTR
        .MergeCells = False
    End With
    Selection.Merge
    Range("A2:G2").Select
    With Selection.Font
        .Name = "Arial"
        .Size = 10
        .Strikethrough = False
        .Superscript = False
        .Subscript = False
        .OutlineFont = False
        .Shadow = False
        .Underline = xlUnderlineStyleNone
        .Color = -16777216
        .TintAndShade = 0
        .ThemeFont = xlThemeFontNone
    End With
    ActiveCell.FormulaR1C1 = Worksheets("Data").Range("F2").Value

    Columns("A:G").Select
    With Selection
        .WrapText = False
    End With

    Range("A3").Select
    ActiveCell.FormulaR1C1 = "Item"

    Range("B3").Select
    ActiveCell.FormulaR1C1 = "Description"

    Range("A4").Select
    ActiveCell.FormulaR1C1 = "Customer Type"

    Range("E4").Select
    ActiveCell.FormulaR1C1 = "Qty"
    With Selection
        .HorizontalAlignment = xlRight
        .VerticalAlignment = xlBottom
        .WrapText = False
        .Orientation = 0
        .AddIndent = False
        .IndentLevel = 0
        .ShrinkToFit = False
        .ReadingOrder = xlLTR
        .MergeCells = False
    End With

    Range("G4").Select
    ActiveCell.FormulaR1C1 = "Amount"
    With Selection
        .HorizontalAlignment = xlRight
        .VerticalAlignment = xlBottom
        .WrapText = False
        .Orientation = 0
        .AddIndent = False
        .IndentLevel = 0
        .ShrinkToFit = False
        .ReadingOrder = xlLTR
        .MergeCells = False
    End With

    Columns("A:D").Select
    Range("A3").Activate
    Selection.ColumnWidth = 20
    Columns("A:A").Select
    Selection.ColumnWidth = 30
    Columns("D:G").ColumnWidth = 15.22

    Range("A3:G4").Select
    With Selection.Interior
        .Pattern = xlSolid
        .PatternColorIndex = xlAutomatic
        .ThemeColor = xlThemeColorDark1
        .TintAndShade = -4.99893185216834E-02
        .PatternTintAndShade = 0
    End With
    Selection.Font.Bold = True
    With Selection.Font
        .Name = "Arial"
        .Size = 10
        .Strikethrough = False
        .Superscript = False
        .Subscript = False
        .OutlineFont = False
        .Shadow = False
        .Underline = xlUnderlineStyleNone
        .Color = -16777216
        .TintAndShade = 0
        .ThemeFont = xlThemeFontNone
    End With
    Rows("5:5").Select
    ActiveWindow.FreezePanes = True



    Range("A1").Select
End Sub

Sub PMPFillReportData()
    'posicion en que se agrega el renglon en el rpt
    Dim iBFila As Long
    iBFila = 5

    'conteo filas en crudo
    Dim iDFila As Long
    iDFila = 2

    Dim iDFilaFin As Long

    Dim i As Integer 'for loop i

    Dim iGroupQty As Integer    'cantidad por grupo
    iGroupQty = 0
    Dim sCurGroupVal As String          'valor del grupo actual
    Dim sCurGroupWhileVal As String     'valor del grupo while actual

    Dim iGroup2Qty As Integer    'cantidad por grupo 2
    iGroup2Qty = 0
    Dim sCurGroup2Val As String         'valor del grupo 2 actual
    Dim sCurGroupWhile2Val As String   'valor del grupo while 2 actual

    Dim dGroupTotal As Double
    Dim dGroup2Total As Double
    Dim dGrandTotal As Double

    Dim iSubGroupTotalQty As Integer
    Dim iGroupTotalQty As Integer
    Dim iGrandTotalQty As Integer

    Dim rng As Range            'rango del grupo
    Dim rng2 As Range

    Worksheets("Rpt").Select
    Cells.Select
    Selection.RowHeight = 15#

    Set rng = Worksheets("Data").Range("A2:A" & iFila)

    sCurGroupVal = Worksheets("Data").Range("A2:A2").Value
    sCurGroupWhileVal = sCurGroupVal
    iGroupQty = WorksheetFunction.CountIf(rng, sCurGroupVal)     'cuantas veces esta el Customer Type  en el rango

    sCurGroup2Val = Worksheets("Data").Range("C2:C2").Value
    sCurGroupWhile2Val = sCurGroup2Val

    While sCurGroupVal = sCurGroupWhileVal And sCurGroupVal <> ""

        Worksheets("Rpt").Range("A" & iBFila).Value = Worksheets("Data").Range("A" & iDFila).Value  'Header Item
        Worksheets("Rpt").Range("A" & iBFila).Font.Bold = True
        Worksheets("Rpt").Range("B" & iBFila).Value = Worksheets("Data").Range("B" & iDFila).Value  'Header Description

        iGroupQty = WorksheetFunction.CountIf(rng, sCurGroupVal)
        iDFilaFin = iDFila + iGroupQty - 1

        ' FIX: Reset anchor BEFORE inner While (moved from inside loop)
        sCurGroup2Val = Worksheets("Data").Range("C" & iDFila).Value
        sCurGroupWhile2Val = sCurGroup2Val

        While sCurGroup2Val = sCurGroupWhile2Val And sCurGroup2Val <> "" And sCurGroupVal = sCurGroupWhileVal
            iBFila = iBFila + 1
            Worksheets("Rpt").Range("A" & iBFila).Value = Worksheets("Data").Range("C" & iDFila).Value 'Customer Type

            Set rng2 = Worksheets("Data").Range("C" & iDFila & ":C" & iDFilaFin)
            ' FIX: Removed these two lines that were here - they reset the anchor inside the loop
            ' sCurGroup2Val = Worksheets("Data").Range("C" & iDFila).Value
            ' sCurGroupWhile2Val = sCurGroup2Val
            iGroup2Qty = WorksheetFunction.CountIf(rng2, sCurGroup2Val)

            For i = 1 To iGroup2Qty
                iSubGroupTotalQty = iSubGroupTotalQty + Worksheets("Data").Range("D" & iDFila).Value 'Sum Qty
                dGroup2Total = dGroup2Total + Worksheets("Data").Range("E" & iDFila).Value 'Sum Total

                iDFila = iDFila + 1
            Next

            Worksheets("Rpt").Range("E" & iBFila).Value = iSubGroupTotalQty
            Worksheets("Rpt").Range("E" & iBFila).NumberFormat = "0"
            Worksheets("Rpt").Range("G" & iBFila).Value = dGroup2Total
            Worksheets("Rpt").Range("G" & iBFila).Select
            Selection.HorizontalAlignment = xlRight
            Selection.NumberFormat = "[$-409]#,##0.00"

            dGroupTotal = dGroupTotal + dGroup2Total
            iGroupTotalQty = iGroupTotalQty + iSubGroupTotalQty

            'Grab next data set
            sCurGroup2Val = Worksheets("Data").Range("C" & iDFila).Value
            ' FIX: This line was removed - it caused infinite loop
            ' sCurGroupWhile2Val = sCurGroup2Val

            'Check First Grouping still matches
            sCurGroupVal = Worksheets("Data").Range("A" & iDFila).Value

            iSubGroupTotalQty = 0
            dGroup2Total = 0
        Wend

        iBFila = iBFila + 1
        dGrandTotal = dGrandTotal + dGroupTotal
        iGrandTotalQty = iGrandTotalQty + iGroupTotalQty

        Worksheets("Rpt").Range("D" & iBFila).Value = sCurGroupWhileVal
        Worksheets("Rpt").Range("D" & iBFila).Select
        Call FormatTotalHeader

        Worksheets("Rpt").Range("E" & iBFila).Value = iGroupTotalQty
        Worksheets("Rpt").Range("E" & iBFila).Select
        Call FormatTotal
        Selection.NumberFormat = "0"

        ' Worksheets("Rpt").Range("F" & iBFila).Value = sCurGroupVal
        ' Worksheets("Rpt").Range("F" & iBFila).Select
        ' Call FormatTotalHeader

        Worksheets("Rpt").Range("G" & iBFila).Value = dGroupTotal
        Worksheets("Rpt").Range("G" & iBFila).Select
        Call FormatTotal

        iBFila = iBFila + 1

        Worksheets("Rpt").Select

        'Load next in group
        sCurGroupVal = Worksheets("Data").Range("A" & iDFila).Value
        iGroupQty = WorksheetFunction.CountIf(rng, sCurGroupVal)
        dGroupTotal = 0
        iGroupTotalQty = 0
        sCurGroupWhileVal = sCurGroupVal
    Wend

    iBFila = iBFila + 1

    Worksheets("Rpt").Range("D" & iBFila).Value = "Grand Total"
    Worksheets("Rpt").Range("D" & iBFila).Select
    Call FormatTotalHeader

    Worksheets("Rpt").Range("E" & iBFila).Value = iGrandTotalQty
    Worksheets("Rpt").Range("E" & iBFila).Select
    Call FormatTotal
    Selection.NumberFormat = "0"

    Worksheets("Rpt").Range("G" & iBFila).Value = dGrandTotal
    Worksheets("Rpt").Range("G" & iBFila).Select
    Call FormatTotal

    Range("A1").Select

    iBFila = 0
    iDFila = 0
    sCurGroupVal = ""
    dGranTotal = 0
    Set rng = Nothing
    Set rng2 = Nothing
End Sub

Sub PMPOrdenoCrudo()
    '
    ' PMPOrdenoCrudo Macro
    '
    Worksheets("Data").Select

    iFila = ActiveSheet.UsedRange.SpecialCells(xlCellTypeLastCell).Row

    ActiveWorkbook.Worksheets("Data").Sort.SortFields.Clear
    ActiveWorkbook.Worksheets("Data").Sort.SortFields.Add Key:=Range("A2:A" & iFila) _
        , SortOn:=xlSortOnValues, Order:=xlAscending, DataOption:=xlSortNormal
    ActiveWorkbook.Worksheets("Data").Sort.SortFields.Add Key:=Range("C2:C" & iFila) _
        , SortOn:=xlSortOnValues, Order:=xlAscending, DataOption:=xlSortNormal

    With ActiveWorkbook.Worksheets("Data").Sort
        .SetRange Range("A1:G" & iFila)
        .Header = xlYes
        .MatchCase = False
        .Orientation = xlTopToBottom
        .SortMethod = xlPinYin
        .Apply
    End With
End Sub

Sub Formato_americano()
 With Application
    .DecimalSeparator = "."
    .ThousandsSeparator = ","
    .UseSystemSeparators = False
 End With
End Sub

Sub FormatTotal()
    With Selection.Interior
        .Pattern = xlSolid
        .PatternColorIndex = xlAutomatic
        .ThemeColor = xlThemeColorDark1
        .TintAndShade = -4.99893185216834E-02
        .PatternTintAndShade = 0
    End With
    Selection.HorizontalAlignment = xlRight
    Selection.NumberFormat = "[$-409]#,##0.00"
End Sub

Sub FormatTotalHeader()
    With Selection
        .HorizontalAlignment = xlRight
        .VerticalAlignment = xlCenter
        .WrapText = False
        .Orientation = 0
        .AddIndent = False
        .IndentLevel = 0
        .ShrinkToFit = False
        .ReadingOrder = xlLTR
        .MergeCells = False
    End With
    Selection.Font.Bold = True
End Sub
