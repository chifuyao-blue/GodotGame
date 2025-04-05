extends Node
@onready var slime = $"../../slime"
@onready var slime_2 = $"../../slime2"
@onready var slime_3 = $"../../slime3"


var sl2_1 = 0
var sl2_2 = 0
var sl2_3 = 0

func _ready():
	if has_save():
		_load()
	
func _load() -> void:
	var data = FileAccess.open("user://saveslime.tres",FileAccess.READ) 
	sl2_1 = data.get_var()
	sl2_2 = data.get_var()
	sl2_3 = data.get_var()
	if sl2_1 == 1:
		slime.queue_free()
	if sl2_2 == 1:
		slime_2.queue_free()
	if sl2_3 == 1:
		slime_3.queue_free()
	
func _save() -> void:
	var file = FileAccess.open("user://saveslime.tres",FileAccess.WRITE)
	file.store_var(sl2_1)
	file.store_var(sl2_2)
	file.store_var(sl2_3)
	file.close()
	
func has_save() -> bool:
	var save_path = "user://saveslime.tres"
	return FileAccess.file_exists(save_path)

func _sl1():
	sl2_1 = 1
	
func _sl2():
	sl2_2 = 1
	
func _sl3():
	sl2_3 = 1
	
	
