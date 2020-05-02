# pynake

pynakeはpyxelを用いて作られたシンプルなヘビゲームです。

pythonのロゴ(青と黄の二匹のヘビ)がモチーフになっています。
 
# DEMO
 
実際にプレイしてみるとこんな感じです。
 
![demo](https://raw.github.com/wiki/sirococoa/pynake/images/pynake_demo.gif)
 
二匹のヘビは対称的な動きをしています。

操作が反転することになるため、パズルゲームのような頭を使うゲームとなっています。
 
# Features
 
pynakeは[pyxel](https://github.com/kitao/pyxel)を使って作られています。
 
```python
import pyxel
```
[Pyxel](https://github.com/kitao/pyxel)はシンプルで使いやすいゲームエンジンです。

レトロゲームや簡単なミニゲームを作るのに適しています。
 
# Requirement
 
* pyxel 1.3.1
 
# Installation
 
pipを使ってpyxelをインストールしてください。
 
```bash
pip install pyxel
```
 
# Usage

[itch io](https://sirococoa.itch.io/pynake)上で実行ファイルを公開しています。

windowsの環境があり、ゲームを試したいだけの方は上記サイトからダウンロードして遊ぶことができます。

それ以外の場合、ソースコードから直接実行する方法もあります。

1. main.pyとassets/pynake.pyxresを同じディレクトリに用意してください。
 
2. main.pyを実行してください。
 
```bash
python main.py
```
 
# Note
 
LinuxとMacの環境では動作を試していません。
 
# Author
 
* sirococoa
* Twitter : @sirococoa1
 
# License
 
pynakeは[MIT license](https://en.wikipedia.org/wiki/MIT_License)です。
 
