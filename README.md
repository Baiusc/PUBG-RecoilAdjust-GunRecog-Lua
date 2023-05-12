# PUBG_gunRecognition_recoilControl
In pubg , automatic recognition of gun and accessories,  gun pressure (recoil control),ballistic table

```json
"m762_zl":[
      {"x": 0, "y": 3, "d": 2},
      {"x": 0, "y": 2, "d": 2}],
```

满配 m762
```lua
 {1, 0},
      {2, 44},
      {3, 24},
	{4, 27},
      {5, 29},
	{6, 36},
	{7, 36},
	{8, 37},
	{9, 39},
      {10, 39},
	{11, 40},
	{12, 42},
{13, 41},
{14, 42},
      {15, 45},
    {16, 45},
    {17, 46},
    {18, 47},
    {19, 46},
  {20, 47},
  {21, 48},
  {22, 47},
  {23, 48},
 {24, 48},
  {25, 50},
  {26, 48},
  {27, 51},
  {28, 50},
  {29, 48},
      {30, 47},
  {31, 47},
    {32, 48},
    {33, 48},
    {34, 48},
    {35, 48},
    {36, 48},
    {37, 48},
    {38, 48},
    {39, 48},
   {40, 48},
   {41, 48},
      {42, 51},
```

裸配m762
```lua
 {1, 0},
      {2, 44},
      {3, 34},
	{4, 37},
      {5, 39},
	{6, 42},
	{7, 46},
	{8, 42},
	{9, 45},
      {10, 55},
	{11, 56},
	{12, 54},
{13, 55},
{14, 56},
      {15, 54},
    {16, 55},
    {17, 62},
    {18, 63},
    {19, 62},
  {20, 63},
  {21, 62},
  {22, 63},
  {23, 62},
 {24, 63},
  {25, 62},
  {26, 63},
  {27, 62},
  {28, 63},
  {29, 62},
      {30, 63},
  {31, 62},
    {32, 63},
    {33, 62},
    {34, 63},
    {35, 62},
    {36, 63},
    {37, 62},
    {38, 63},
    {39, 67},
   {40, 68},
   {41, 67},
      {42, 68},
```
我需要将m762_zl = {{x=0, y=3, d=2}, {x=0, y=2, d=2}}这样的数据转换为      "m762_zl": [
        {"x": 0, "y": 3, "d": 2},
        {"x": 0, "y": 2, "d": 2}],这样的json格式。请你帮我写一个python函数，来完成此需求


m762站姿裸配精调弹道表
```lua
m762_zl = {{x=0, y=3, d=2}, {x=0, y=2, d=2}, {x=0, y=2, d=2}, {x=0, y=2, d=2}, {x=0, y=2, d=2}, {x=0, y=2, d=2}, {x=0, y=2, d=2}, {x=0, y=2, d=3}, {x=0, y=2, d=3}, {x=0, y=2, d=3}, {x=0, y=2, d=3}, {x=0, y=2, d=3}, {x=0, y=8, d=16}, {x=0, y=8, d=16}, {x=0, y=8, d=16}, {x=0, y=8, d=16}, {x=0, y=8, d=17}, {x=0, y=8, d=17}, {x=0, y=7, d=17}, {x=0, y=7, d=17}, {x=0, y=7, d=17}, {x=0, y=7, d=17}, {x=0, y=7, d=17}, {x=0, y=7, d=17}, {x=0, y=8, d=16}, {x=0, y=8, d=16}, {x=0, y=8, d=16}, {x=0, y=8, d=16}, {x=0, y=8, d=16}, {x=0, y=8, d=17}, {x=0, y=7, d=17}, {x=0, y=7, d=17}, {x=0, y=7, d=17}, {x=0, y=7, d=17}, {x=0, y=7, d=17}, {x=0, y=7, d=17}, {x=0, y=9, d=16}, {x=0, y=9, d=16}, {x=0, y=9, d=16}, {x=0, y=9, d=16}, {x=0, y=9, d=17}, {x=0, y=9, d=17}, {x=0, y=8, d=17}, {x=0, y=8, d=17}, {x=0, y=8, d=17}, {x=0, y=8, d=17}, {x=0, y=8, d=17}, {x=0, y=8, d=17}, {x=0, y=10, d=16}, {x=0, y=10, d=16}, {x=0, y=10, d=16}, {x=0, y=10, d=16}, {x=0, y=10, d=16}, {x=0, y=9, d=17}, {x=0, y=9, d=17}, {x=0, y=9, d=17}, {x=0, y=9, d=17}, {x=0, y=9, d=17}, {x=0, y=9, d=17}, {x=0, y=9, d=17}, {x=0, y=11, d=16}, {x=0, y=11, d=16}, {x=0, y=11, d=16}, {x=0, y=11, d=16}, {x=0, y=11, d=16}, {x=0, y=11, d=17}, {x=0, y=11, d=17}, {x=0, y=10, d=17}, {x=0, y=10, d=17}, {x=0, y=10, d=17}, {x=0, y=10, d=17}, {x=0, y=10, d=17}, {x=0, y=12, d=16}, {x=0, y=12, d=16}, {x=0, y=12, d=16}, {x=0, y=11, 
d=16}, {x=0, y=11, d=17}, {x=0, y=11, d=17}, {x=0, y=11, d=17}, {x=0, y=11, d=17}, {x=0, y=11, d=17}, {x=0, y=11, d=17}, {x=0, y=11, d=17}, {x=0, y=11, d=17}, {x=0, y=12, d=16}, {x=0, y=12, d=16}, {x=0, y=12, d=16}, {x=0, y=11, d=16}, {x=0, y=11, d=16}, {x=0, y=11, d=17}, {x=0, y=11, d=17}, {x=0, y=11, d=17}, {x=0, y=11, d=17}, {x=0, y=11, d=17}, {x=0, y=11, d=17}, {x=0, y=11, d=17}, {x=0, y=12, 
d=16}, {x=0, y=12, d=16}, {x=0, y=12, d=16}, {x=0, y=12, d=16}, {x=0, y=12, d=17}, {x=0, y=12, d=17}, {x=0, y=11, d=17}, {x=0, y=11, d=17}, {x=0, y=11, d=17}, {x=0, y=11, d=17}, {x=0, y=11, d=17}, {x=0, y=11, d=17}, {x=0, y=12, d=16}, {x=0, y=12, d=16}, {x=0, y=12, 
d=16}, {x=0, y=12, d=16}, {x=0, y=12, d=16}, {x=0, y=11, d=17}, {x=0, y=11, d=17}, {x=0, y=11, d=17}, {x=0, y=11, d=17}, {x=0, y=11, d=17}, {x=0, y=11, d=17}, {x=0, y=11, d=17}, {x=0, y=12, d=16}, {x=0, y=11, d=16}, {x=0, y=11, d=16}, {x=0, y=11, d=16}, {x=0, y=11, d=16}, {x=0, y=11, d=17}, {x=0, y=11, d=17}, {x=0, y=11, d=17}, {x=0, y=11, d=17}, {x=0, y=11, d=17}, {x=0, y=11, d=17}, {x=0, y=11, d=17}, {x=0, y=12, d=16}, {x=0, y=12, d=16}, {x=0, y=12, d=16}, {x=0, y=11, d=16}, {x=0, y=11, d=17}, {x=0, y=11, d=17}, {x=0, y=11, d=17}, {x=0, y=11, d=17}, {x=0, y=11, d=17}, {x=0, y=11, d=17}, {x=0, y=11, d=17}, {x=0, y=11, d=17}, {x=0, y=13, d=16}, {x=0, y=12, 
d=16}, {x=0, y=12, d=16}, {x=0, y=12, d=16}, {x=0, y=12, d=16}, {x=0, y=12, d=17}, {x=0, y=12, d=17}, {x=0, y=12, d=17}, {x=0, y=12, d=17}, {x=0, y=12, d=17}, {x=0, y=12, d=17}, {x=0, y=12, d=17}, {x=0, y=13, d=16}, {x=0, y=13, d=16}, {x=0, y=13, d=16}, {x=0, y=13, d=16}, {x=0, y=13, d=17}, {x=0, y=13, d=17}, {x=0, y=12, d=17}, {x=0, y=12, d=17}, {x=0, y=12, d=17}, {x=0, y=12, d=17}, {x=0, y=12, d=17}, {x=0, y=12, d=17}, {x=0, y=13, d=16}, {x=0, y=13, d=16}, {x=0, y=13, d=16}, {x=0, y=13, d=16}, {x=0, y=13, d=16}, {x=0, y=13, 
d=17}, {x=0, y=12, d=17}, {x=0, y=12, d=17}, {x=0, y=12, d=17}, {x=0, y=12, d=17}, {x=0, y=12, d=17}, {x=0, y=12, d=17}, {x=0, y=13, d=16}, {x=0, y=13, d=16}, {x=0, y=13, d=16}, {x=0, y=13, d=16}, {x=0, y=13, d=16}, {x=0, y=13, d=17}, {x=0, y=12, d=17}, {x=0, y=12, d=17}, {x=0, y=12, d=17}, {x=0, y=12, d=17}, {x=0, y=12, d=17}, {x=0, y=12, d=17}, {x=0, y=13, d=16}, {x=0, y=13, d=16}, {x=0, y=13, d=16}, {x=0, y=13, d=16}, {x=0, y=13, d=17}, {x=0, y=13, d=17}, {x=0, y=12, d=17}, {x=0, y=12, d=17}, {x=0, y=12, d=17}, {x=0, y=12, d=17}, {x=0, y=12, d=17}, {x=0, y=12, d=17}, {x=0, y=13, d=16}, {x=0, y=13, d=16}, {x=0, y=13, d=16}, {x=0, y=13, d=16}, {x=0, y=13, d=16}, {x=0, y=13, d=17}, {x=0, y=13, d=17}, {x=0, y=13, d=17}, {x=0, y=12, d=17}, {x=0, y=12, d=17}, {x=0, y=12, d=17}, {x=0, y=12, 
d=17}, {x=0, y=7, d=16}, {x=0, y=7, d=16}, {x=0, y=7, d=16}, {x=0, y=7, d=16}, {x=0, y=7, d=17}, {x=0, y=7, d=17}, {x=0, y=7, d=17}, {x=0, y=7, d=17}, {x=0, y=7, d=17}, {x=0, y=7, d=17}, {x=0, y=6, d=17}, {x=0, y=6, d=17}, {x=0, y=7, d=16}, {x=0, y=7, d=16}, {x=0, y=7, d=16}, {x=0, y=7, d=16}, {x=0, y=7, d=16}, {x=0, y=7, d=17}, {x=0, y=7, d=17}, {x=0, y=7, d=17}, {x=0, y=7, d=17}, {x=0, y=7, d=17}, {x=0, y=6, d=17}, {x=0, y=6, d=17}, {x=0, y=7, d=16}, {x=0, y=7, d=16}, {x=0, y=7, d=16}, {x=0, y=7, d=16}, {x=0, y=7, d=16}, {x=0, y=7, d=17}, {x=0, y=7, d=17}, {x=0, y=7, d=17}, {x=0, y=7, d=17}, {x=0, y=7, d=17}, {x=0, y=6, d=17}, {x=0, y=6, d=17}, {x=0, y=0, d=16}, {x=0, y=0, d=16}, 
{x=0, y=0, d=16}, {x=0, y=0, d=16}, {x=0, y=0, d=17}, {x=0, y=0, d=17}, {x=0, y=0, d=17}, {x=0, y=0, d=17}, {x=0, y=0, d=17}, {x=0, y=0, d=17}, {x=0, y=0, d=17}, {x=0, y=0, d=17}, {x=0, y=0, d=16}, {x=0, y=0, d=16}, {x=0, y=0, d=16}, {x=0, y=0, d=16}, {x=0, y=0, d=16}, {x=0, y=0, d=17}, {x=0, y=0, d=17}, {x=0, y=0, d=17}, {x=0, y=0, d=17}, {x=0, y=0, d=17}, {x=0, y=0, d=17}, {x=0, y=0, d=17}, {x=0, y=0, d=16}, {x=0, y=0, d=16}, {x=0, y=0, d=16}, {x=0, y=0, d=16}, {x=0, y=0, d=17}, {x=0, y=0, d=17}, {x=0, y=0, d=17}, {x=0, y=0, d=17}, {x=0, y=0, d=17}, {x=0, y=0, d=17}, {x=0, y=0, d=17}, {x=0, y=0, d=17}, {x=0, y=0, d=16}, {x=0, y=0, d=16}, {x=0, y=0, d=16}, {x=0, y=0, d=16}, {x=0, y=0, d=16}, {x=0, y=0, d=17}, {x=0, y=0, d=17}, {x=0, y=0, d=17}, {x=0, y=0, d=17}, {x=0, y=0, d=17}, {x=0, y=0, d=17}, {x=0, y=0, d=17}, {x=0, y=0, d=16}, {x=0, y=0, d=16}, {x=0, y=0, d=16}, {x=0, y=0, d=16}, {x=0, y=0, d=16}, {x=0, y=0, d=17}, {x=0, y=0, d=17}, {x=0, y=0, d=17}, {x=0, y=0, d=17}, {x=0, y=0, d=17}, {x=0, y=0, d=17}, {x=0, y=0, d=17}, {x=0, y=0, d=16}, {x=0, y=0, d=16}, {x=0, y=0, d=16}, {x=0, y=0, d=16}, {x=0, y=0, d=17}, {x=0, y=0, d=17}, {x=0, y=0, d=17}, {x=0, y=0, d=17}, {x=0, y=0, d=17}, {x=0, y=0, d=17}, {x=0, y=0, d=17}, {x=0, y=0, d=17}, {x=0, y=0, d=16}, {x=0, y=0, d=16}, {x=0, y=0, d=16}, {x=0, y=0, d=16}, {x=0, y=0, d=16}, {x=0, y=0, d=17}, {x=0, y=0, d=17}, {x=0, y=0, d=17}, {x=0, y=0, d=17}, {x=0, y=0, d=17}, {x=0, y=0, d=17}, {x=0, y=0, d=17}, {x=0, y=0, d=16}, {x=0, y=0, d=16}, {x=0, y=0, d=16}, {x=0, y=0, d=16}, {x=0, y=0, d=17}, {x=0, y=0, d=17}, {x=0, y=0, d=17}, {x=0, y=0, d=17}, {x=0, y=0, d=17}, {x=0, y=0, d=17}, {x=0, y=0, d=17}, {x=0, y=0, d=17}, {x=0, y=0, d=16}, {x=0, y=0, d=16}, {x=0, y=0, d=16}, {x=0, y=0, d=16}, {x=0, y=0, d=16}, {x=0, y=0, d=17}, {x=0, y=0, d=17}, {x=0, y=0, d=17}, {x=0, y=0, d=17}, {x=0, y=0, d=17}, {x=0, y=0, d=17}, {x=0, y=0, d=17}}

```
