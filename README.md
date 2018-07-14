# Astar_Sliding_Puzzle

## Usage ##
python solver.py inputfile.txt
### python version = 2.7

## 結果 ##
move シーケンスはBlankの移動位置、一番左上は（1,1）

## What's this ##
４ｘ３のタイルパズルを解くソルバ(4x3以外も解ける)。
通常のタイルパズルは４ｘ４あるいは３ｘ３であるがここでは４ｘ３のソルバを書く。

目的状態：(0はblank)
0 1 2
3 4 5
6 7 8
9 10 11

探索アルゴリズムはA star。
ヒューリスティック関数としてマンハッタン距離を実装すること。
パズルの初期状態を入力とする。
solver inputfile.txt

inputfileの内容例：
例えば初期状態が
1 3 5
7 9 11
2 4 6
8 0  10    (0はblank)
の場合、
inputfile.txt   は　　1 3 5 7 9 11 2 4 6 8 0 10
