import Funiture
StrctureList={
0:'WoodenFloor',
1:'WoodenWall',
}
FunitureList={
0:None,
1:Funiture.Door(0,0,0),
}

BuildingList={#方便创建 统一为[y][x]
'Residence':
	{
	'Structure':
		[
		[1,1,1,1],
		[1,0,0,1],
		[1,0,0,1],
		[1,0,1,1]
		],
    'Funiture':
		[
		[0,0,0,0],
		[0,0,0,0],
		[0,0,0,0],
		[0,1,0,0]
		]
}


}