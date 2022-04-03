% Al Danial, David Garrison
% This version works with MATLAB 2020b and newer
% Note: 2020b requires Pyton v3.7 or v3.8
OP = imp("openpyxl");
styles = imp("openpyxl.styles");
Font = styles.Font;
Alignment = styles.Alignment;
PatternFill = styles.PatternFill;
book = OP.Workbook();
sheet = book.active;
sheet.title = "Pets by weight";

% font styles, background color
ft_title = Font(...
    pyargs("name","Arial", ...
    "size",int64(14),"bold",py.True));
ft_red = Font(pyargs("color","00FF0000"));
ft_italics = Font(pyargs("bold",py.True,...
                  "italic",py.True));
bg_green = PatternFill( pyargs(...
    "fgColor","C5FD2F","fill_type","solid"));

sheet.merge_cells("B2:D3");
B2 = sheet.cell(2,2);
B2.value = "My Pets";
B2.font = ft_title;
B2.alignment = Alignment(pyargs(...
 "horizontal","center","vertical","center"));

% column headings
category={"Name","Animal","weight [kg]"};
row = int64(4); col = int64(1);
for i = 1:length(category)
  nextCell = sheet.cell(row, col+i);
  nextCell.value = category{i};
  nextCell.fill = bg_green;
end

pets = {{"Nutmeg", "Rabbit", 2.5},...
        {"Annabel", "Dog", 4.3},  ...
        {"Sunny", "Bird", 0.02},  ...
        {"Harley", "Dog", 17.1},  ...
        {"Toby", "Dog", 24.0},    ...
        {"Mr Socks", "Cat", 3.9}};

for P = pets
  row = row + 1;
  for j = 1:length(category)
    sheet.cell(row,col+j,P{1}{j});
    if j == 3 && P{1}{j} < 0.1
      nextCell = sheet.cell(row,col+j);
      nextCell.font = ft_red;
    end
  end
end

% equation to sum all weights
eqn = sprintf("=SUM(D4:D%d)", row);
nextCell = sheet.cell(row+1, 4);
nextCell.value = eqn;

nextCell = sheet.cell(row+1, 2);
nextCell.value = "Total weight:";
nextCell.font = ft_italics;

book.save("pets.xlsx")
