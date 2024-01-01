from mcpi.minecraft import Minecraft
from mcpi import block

def fill_area(mc, block_id):
	x_start, x_end = -215, -209
	z_start, z_end = -227, -117
	y_start, y_end = 40, 59
	
	mc.setBlocks(x_start, y_start, z_start, x_end, y_end, z_end, block_id)


def main():
	host = "192.168.1.6"
	port = 4711
	user = "alex"
	x = -923 # -215
	y = 106
	z = 466
	mc = Minecraft.create(host, port)
	mc.setBlock(x, y, z, block.GRASS.id)
	# fill_area(mc, block.SAND.id)


if __name__ == '__main__':
	main()