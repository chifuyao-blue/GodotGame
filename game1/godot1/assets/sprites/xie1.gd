extends CanvasLayer
@onready var texture_rect_2 = $TextureRect2
@onready var texture_rect_3 = $TextureRect3
@onready var texture_rect_4 = $TextureRect4


var sc1 = 0
var xl1 = 0
var xl2 = 0
var xl3 = 0


func has_save() -> bool:
	var save_path = "user://savexie.tres"
	return FileAccess.file_exists(save_path)
	
func _load_xie():
	print("_load_xie运行了！！！！！")
	var data3 = FileAccess.open("user://savexie.tres",FileAccess.READ) 
	sc1 = data3.get_var()
	xl1 = data3.get_var()
	xl2 = data3.get_var()
	xl3 = data3.get_var()
	print("第一格血：",xl3)
	if xl1 == 1:
		texture_rect_2.hide()
	if xl2 == 1:
		texture_rect_3.hide()
	if  xl3 == 1:
		texture_rect_4.hide()

# Called when the node enters the scene tree for the first time.
func _ready():
	if has_save():
		_load_xie()
	
	 # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass
