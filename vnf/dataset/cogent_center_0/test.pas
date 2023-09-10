program Dem_chu;

var
  inputFile, outputFile: Text;
  str: string;
  count: integer;

function La_chu(c: char): boolean;
  begin
    La_chu := (c >= 'a') and (c <= 'z') or (c >= 'A') and (c <= 'Z');
  end;

begin
  Assign(inputFile, 'string.inp');
  Reset(inputFile);
  Assign(outputFile, 'string.out');
  Rewrite(outputFile);
 
  Readln(inputFile, str);
  count := 0;
  for var i := 1 to Length(str) do
    if La_chu(str[i]) then
      Inc(count);

  Writeln(outputFile, count);
  Close(inputFile);
  Close(outputFile);
end.
