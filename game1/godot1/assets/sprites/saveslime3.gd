extends Node

@onready var slime = $"../../slime"
@onready var slime_2 = $"../../slime2"
@onready var slime_3 = $"../../slime3"
@onready var slime_4 = $"../../slime4"
@onready var slime_5 = $"../../slime5"
@onready var slime_6 = $"../../slime6"
@onready var slime_7 = $"../../slime7"


var sl3_1 = 0
var sl3_2 = 0
var sl3_3 = 0
var sl3_4 = 0
var sl3_5 = 0
var sl3_6 = 0
var sl3_7 = 0


func _ready():
	if has_save():
		_load()
	
func _load() -> void:
	var data = FileAccess.open("user://saveslime.tres",FileAccess.READ) 
	sl3_1 = data.get_var()
	sl3_2 = data.get_var()
	sl3_3 = data.get_var()
	sl3_4 = data.get_var()
	sl3_5 = data.get_var()
	sl3_6 = data.get_var()
	sl3_7 = data.get_var()
	
	if sl3_1 == 1:
		slime.queue_free()
	if sl3_2 == 1:
		slime_2.queue_free()
	if sl3_3 == 1:
		slime_3.queue_free()
	if sl3_4 == 1:
		slime_4.queue_free()
	if sl3_5 == 1:
		slime_5.queue_free()
	if sl3_6 == 1:
		slime_6.queue_free()
	if sl3_7 == 1:
		slime_7.queue_free()

	
func _save() -> void:
	var file = FileAccess.open("user://saveslime.tres",FileAccess.WRITE)
	file.store_var(sl3_1)
	file.store_var(sl3_2)
	file.store_var(sl3_3)
	file.store_var(sl3_4)
	file.store_var(sl3_5)
	file.store_var(sl3_6)
	file.store_var(sl3_7)
	file.close()
	
func has_save() -> bool:
	var save_path = "user://saveslime.tres"
	return FileAccess.file_exists(save_path)

func _sl1():
	sl3_1 = 1
	
func _sl2():
	sl3_2 = 1
	
func _sl3():
	sl3_3 = 1
	
func _sl4():
	sl3_4 = 1
	
func _sl5():
	sl3_5 = 1
	
func _sl6():
	sl3_6 = 1
	
func _sl7():
	sl3_7 = 1
