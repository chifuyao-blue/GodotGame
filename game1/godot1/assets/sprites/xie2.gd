extends CanvasLayer

@onready var xl_1 = $xl1
@onready var xl_2 = $xl2
@onready var xl_3 = $xl3

var sc1 = 0
var xl1 = 0
var xl2 = 0
var xl3 = 0


# Called when the node enters the scene tree for the first time.
func _ready():
	if has_savexie2():
		_savexie2()
	 # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass

func _savexie2():
	var data2 = FileAccess.open("user://savexie.tres",FileAccess.READ)
	sc1 = data2.get_var()
	xl1 = data2.get_var()
	xl2 = data2.get_var()
	xl3 = data2.get_var()
	if xl1 == 1:
		xl_1.hide()
	if xl2 == 1:
		xl_2.hide()
	if xl3 == 1:
		xl_3.hide()
		
func has_savexie2() -> bool:
	var save_path = "user://savexie.tres"
	return FileAccess.file_exists(save_path)
