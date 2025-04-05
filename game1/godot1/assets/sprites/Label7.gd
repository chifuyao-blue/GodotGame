extends Label
@onready var label_7 = $"."

@onready var coin = $"../../../../coin/Coin"
@onready var coin_2 = $"../../../../coin/Coin2"
@onready var coin_3 = $"../../../../coin/Coin3"
@onready var coin_4 = $"../../../../coin/Coin4"
@onready var coin_5 = $"../../../../coin/Coin5"
@onready var coin_6 = $"../../../../coin/Coin6"
@onready var coin_7 = $"../../../../coin/Coin7"
@onready var coin_8 = $"../../../../coin/Coin8"

var co1 = 0
var co2 = 0
var co3 = 0
var co4 = 0
var co5 = 0
var co6 = 0
var co7 = 0
var co8 = 0




var score = 0

# Called when the node enters the scene tree for the first time.
func _ready():
	if has_save_chan():
		_chandi1()
	if has_save():
		_load_save()
	 # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass

func add_point():
	score = score + 1
	#print(score)
	label_7.text = str(score)

func _huixie1():
	if score >= 4:
		score = score - 4
		label_7.text = str(score)
		return 1
	else :
		return 2
		
		
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
	
func _co7():
	co7 = 1
	
func _co8():
	co8 = 1
	

	
func _save() -> void:
	var file = FileAccess.open("user://savescore.tres",FileAccess.WRITE)
	file.store_var(score)
	file.close()
	var file2 = FileAccess.open("user://savecoin.tres",FileAccess.WRITE)
	file2.store_var(co1)
	file2.store_var(co2)
	file2.store_var(co3)
	file2.store_var(co4)
	file2.store_var(co5)
	file2.store_var(co6)
	file2.store_var(co7)
	file2.store_var(co8)
	file2.close()
func _load_save():
	var data = FileAccess.open("user://savescore.tres",FileAccess.READ) 
	score = data.get_var()
	label_7.text = str(score)
	var data2 = FileAccess.open("user://savecoin.tres",FileAccess.READ)
	co1 = data2.get_var()
	co2 = data2.get_var()
	co3 = data2.get_var()
	co4 = data2.get_var()
	co5 = data2.get_var()
	co6 = data2.get_var()
	co7 = data2.get_var()
	co8 = data2.get_var()
	if co6 == 1:
		coin_6.queue_free()
	if co7 == 1:
		coin_7.queue_free()
	if co8 == 1:
		coin_8.queue_free()
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
	
func  _chandi1() :
	var data = FileAccess.open("user://chuan.tres",FileAccess.READ) 
	score = data.get_var()
	label_7.text = str(score)
		
func has_save_chan() -> bool:
	var save_path = "user://chuan.tres"
	return FileAccess.file_exists(save_path)
	
func has_save() -> bool:
	var save_path = "user://savescore.tres"
	return FileAccess.file_exists(save_path)

# Called when the node enters the scene tree for the first time.
