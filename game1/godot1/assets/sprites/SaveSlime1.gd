extends Node
@onready var slime_2 = $"../../slime2"

var sl1 = 0


func _ready():
	if has_save():
		_load()
	
func _load() -> void:
	var data = FileAccess.open("user://saveslime.tres",FileAccess.READ) 
	sl1 = data.get_var()
	print("怪的存入！！！！！！！！！！！")
	if sl1 == 1:
		slime_2.queue_free()
	
func _save() -> void:
	var file = FileAccess.open("user://saveslime.tres",FileAccess.WRITE)
	file.store_var(sl1)
	file.close()
	
func has_save() -> bool:
	var save_path = "user://saveslime.tres"
	return FileAccess.file_exists(save_path)

func _sl1():
	sl1 = 1
