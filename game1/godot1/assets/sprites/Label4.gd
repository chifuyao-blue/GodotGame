
extends Label
class_name Label4_1
var score = 0
@onready var label_4 = $"."

@onready var texture_rect_2 = $"../../TextureRect2"
@onready var texture_rect_3 = $"../../TextureRect3"
@onready var texture_rect_4 = $"../../TextureRect4"


@onready var coin = $"../../../../Coins/Coin"
@onready var coin_2 = $"../../../../Coins/Coin2"
@onready var coin_3 = $"../../../../Coins/Coin3"
@onready var coin_4 = $"../../../../Coins/Coin4"
@onready var coin_5 = $"../../../../Coins/Coin5"
@onready var coin_6 = $"../../../../Coins/Coin6"



var co1 = 0
var co2 = 0
var co3 = 0
var co4 = 0
var co5 = 0
var co6 = 0

var sc1 = 0
var xl1 = 0
var xl2 = 0
var xl3 = 0



func _chuandi() :
	var file1 = FileAccess.open("user://chuan.tres",FileAccess.WRITE)
	file1.store_var(score)
	file1.close()
	print("传递2：",score)

func _save() -> void:
	var file = FileAccess.open("user://savescore.tres",FileAccess.WRITE)
	print(score)
	file.store_var(score)
	file.close()
	print("saved_score!")
	var file2 = FileAccess.open("user://savecoin.tres",FileAccess.WRITE)
	print("co1的值", co1)
	file2.store_var(co1)
	file2.store_var(co2)
	file2.store_var(co3)
	file2.store_var(co4)
	file2.store_var(co5)
	file2.store_var(co6)
	file2.close()
	print("save_coin!")
	
	
func _load() -> void:
	var data = FileAccess.open("user://savescore.tres",FileAccess.READ) 
	score = data.get_var()
	print(score)
	label_4.text = str(score)
	print("loaded_score!")
	var data2 = FileAccess.open("user://savecoin.tres",FileAccess.READ)
	co1 = data2.get_var()
	co2 = data2.get_var()
	co3 = data2.get_var()
	co4 = data2.get_var()
	co5 = data2.get_var()
	co6 = data2.get_var()
	if co1 == 1:
		coin.queue_free()
	if co2 == 1:
		coin_2.queue_free()
	if co3 == 1:
		coin_3.queue_free()
	if co4 == 1:
		coin_4.queue_free()
	if co5 == 1:
		coin_5.queue_free()
	if co6 == 1:
		coin_6.queue_free()
	print("load_coin!")
	

func has_save() -> bool:
	var save_path = "user://savescore.tres"
	return FileAccess.file_exists(save_path)
# Called when the node enters the scene tree for the first time.
func _ready():
	# Replace with function body.
	#coin.queue_free()
	if has_save():
		_load()
		
func add_point():
	score = score + 1
	#print(score)
	label_4.text = str(score)
	
func _huixie1():
	if score >= 4:
		score = score - 4
		label_4.text = str(score)
		return 1
	else :
		return 2

# Called every frame. 'delta' is the elapsed time since the previous frame.
#func _process(_delta):
	#if Input.is_action_pressed("ui_cancel"):
		#_save()
func _co1():
	co1 = 1
	
	
func _co2():
	co2 = 1
	
func _co3():
	co3 = 1
	
	
func _co4():
	co4 = 1
	
	
func _co5():
	co5 = 1
	
	
func _co6():
	co6 = 1
	
	
	
	
