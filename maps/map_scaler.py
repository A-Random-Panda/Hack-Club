'''
This is a internal tool used to scale maps in size
The map must have no in line comments and be in the format outputted by the despacer

I quickly wrote this in a way that works but really really sucks
So, the code quality sucks, and I copy and pasted from myself a lot
'''
# pylint: skip-file

from ast import literal_eval

def despacer(string:str) -> str:
    '''Removes spaces, assuming that there are no in line comments'''
    string_list = string.split("\n")
    for i in range(len(string_list)):
        if len(string_list[i]) != 0:
            if "#" not in string_list[i]:
                string_list[i]=string_list[i].replace(" ", "").replace(",", ", ").strip()
            else:
                string_list[i]=string_list[i].strip()
    return "\n".join(string_list)

def scaler(string:str, scale_amount:int) -> str:
    '''
    Scales the x and z coordinates in the map
    Only designed to work in my despaced format
    Don't worry about the implementation, it's definitely good code that I put a lot of time into that's really maintainable and fast!
    '''
    string_list = string.splitlines()
    for i in range(len(string_list)):
        scale_tuple_start_index = string_list[i].find("scale=") + len("scale=")
        if scale_tuple_start_index != -1 + len("scale="):
            tuple_section = string_list[i][scale_tuple_start_index:]
            scale_tuple_end_index = tuple_section.find(")")
            tuple_section = tuple_section[:scale_tuple_end_index+1]
            scale_tuple = literal_eval(tuple_section)
            assert isinstance(scale_tuple, tuple)
            new_tuple = str((scale_tuple[0]*scale_amount, scale_tuple[1], scale_tuple[2]*scale_amount))
            string_list[i] = string_list[i][:scale_tuple_start_index]+new_tuple+string_list[i][scale_tuple_end_index+scale_tuple_start_index+1:]
        #I somehow wrote modular code
        scale_tuple_start_index = string_list[i].find("position=") + len("position=")
        if scale_tuple_start_index != -1 + len("position="):
            tuple_section = string_list[i][scale_tuple_start_index:]
            scale_tuple_end_index = tuple_section.find(")")
            tuple_section = tuple_section[:scale_tuple_end_index+1]
            scale_tuple = literal_eval(tuple_section)
            assert isinstance(scale_tuple, tuple)
            new_tuple = str((scale_tuple[0]*scale_amount, scale_tuple[1], scale_tuple[2]*scale_amount))
            string_list[i] = string_list[i][:scale_tuple_start_index]+new_tuple+string_list[i][scale_tuple_end_index+scale_tuple_start_index+1:]
    return "\n".join(string_list)

def scale_height(string:str, scale_amount:int) -> str:
    '''Scales the height of the map'''
    string_list = string.splitlines()
    for i in range(len(string_list)):
        scale_tuple_start_index = string_list[i].find("scale=") + len("scale=")
        if scale_tuple_start_index != -1 + len("scale="):
            tuple_section = string_list[i][scale_tuple_start_index:]
            scale_tuple_end_index = tuple_section.find(")")
            tuple_section = tuple_section[:scale_tuple_end_index+1]
            scale_tuple = literal_eval(tuple_section)
            assert isinstance(scale_tuple, tuple)
            if scale_tuple[1] != 1:
                new_tuple = str((scale_tuple[0], scale_tuple[1]*scale_amount, scale_tuple[2]))
                string_list[i] = string_list[i][:scale_tuple_start_index]+new_tuple+string_list[i][scale_tuple_end_index+scale_tuple_start_index+1:]
        #I somehow wrote modular code
        scale_tuple_start_index = string_list[i].find("position=") + len("position=")
        if scale_tuple_start_index != -1 + len("position="):
            tuple_section = string_list[i][scale_tuple_start_index:]
            scale_tuple_end_index = tuple_section.find(")")
            tuple_section = tuple_section[:scale_tuple_end_index+1]
            scale_tuple = literal_eval(tuple_section)
            assert isinstance(scale_tuple, tuple)
            new_tuple = str((scale_tuple[0], scale_tuple[1]*scale_amount, scale_tuple[2]))
            string_list[i] = string_list[i][:scale_tuple_start_index]+new_tuple+string_list[i][scale_tuple_end_index+scale_tuple_start_index+1:]
        #yup amazing, the variables don't even make sense in the slightest anymore
        scale_tuple_start_index = string_list[i].find("y=") + len("y=")
        if scale_tuple_start_index != -1 + len("y="):
            tuple_section = string_list[i][scale_tuple_start_index:]
            scale_tuple_end_index = tuple_section.find(",")
            tuple_section = tuple_section[:scale_tuple_end_index]
            scale_tuple = literal_eval(tuple_section)
            assert isinstance(scale_tuple, (int, float))
            new_tuple = str(scale_tuple * scale_amount)+","
            string_list[i] = string_list[i][:scale_tuple_start_index]+new_tuple+string_list[i][scale_tuple_end_index+scale_tuple_start_index+1:]
    return "\n".join(string_list)

if __name__ == "__main__":
    map_string = '''#Floor
Entity(model="cube", scale=(60, 1, 40), texture='purg_floor', color=color.white, collider="box"),

#Roof
Entity(model="cube", scale=(60, 1, 40), y=20, texture='purg_roof', color=color.white, collider="box"),

#Walls across x axis
Entity(model="cube", scale=(50, 20, 1), position=(0, 10, 20), texture='purg_bound', color=color.white, collider="box"),
Entity(model="cube", scale=(50, 20, 1), position=(0, 10, -20), texture='purg_bound', color=color.white, collider="box"),
Entity(model="cube", scale=(5, 20, 1), position=(27.5, 10, 2.5), texture='purg_bound', color=color.white, collider="box"),
Entity(model="cube", scale=(5, 20, 1), position=(27.5, 10, -2.5), texture='purg_bound', color=color.white, collider="box"),
Entity(model="cube", scale=(5, 20, 1), position=(-27.5, 10, 2.5), texture='purg_bound', color=color.white, collider="box"),
Entity(model="cube", scale=(5, 20, 1), position=(-27.5, 10, -2.5), texture='purg_bound', color=color.white, collider="box"),

#Walls across z axis
Entity(model="cube", scale=(1, 20, 17.5), position=(25, 10, 11.25), texture='purg_bound', color=color.white, collider="box"),
Entity(model="cube", scale=(1, 20, 17.5), position=(25, 10, -11.25), texture='purg_bound', color=color.white, collider="box"),
Entity(model="cube", scale=(1, 20, 17.5), position=(-25, 10, 11.25), texture='purg_bound', color=color.white, collider="box"),
Entity(model="cube", scale=(1, 20, 17.5), position=(-25, 10, -11.25), texture='purg_bound', color=color.white, collider="box"),
Entity(model="cube", scale=(1, 20, 5), position=(30, 10, 0), texture='purg_bound', color=color.white, collider="box"),
Entity(model="cube", scale=(1, 20, 5), position=(-30, 10, 0), texture='purg_bound', color=color.white, collider="box"),

#near spawn walls
Entity(model="cube", scale=(1, 10, 15), position=(20, 5, 0), texture='purg_wall', color=color.white, collider="box"),
Entity(model="cube", scale=(1, 10, 15), position=(-20, 5, 0), texture='purg_wall', color=color.white, collider="box"),

#Closer walls across z axis
Entity(model="cube", scale=(1, 10, 10), position=(15, 5, 10), texture='purg_wall', color=color.white, collider="box"),
Entity(model="cube", scale=(1, 10, 10), position=(-15, 5, 10), texture='purg_wall', color=color.white, collider="box"),
Entity(model="cube", scale=(1, 10, 10), position=(15, 5, -10), texture='purg_wall', color=color.white, collider="box"),
Entity(model="cube", scale=(1, 10, 10), position=(-15, 5, -10), texture='purg_wall', color=color.white, collider="box"),

#Closer walls across x axis point walls
Entity(model="cube", scale=(12.5, 10, 1), position=(8.75, 5, 15), texture='purg_wall', color=color.white, collider="box"),
Entity(model="cube", scale=(12.5, 10, 1), position=(-8.75, 5, 15), texture='purg_wall', color=color.white, collider="box"),
Entity(model="cube", scale=(12.5, 10, 1), position=(8.75, 5, -15), texture='purg_wall', color=color.white, collider="box"),
Entity(model="cube", scale=(12.5, 10, 1), position=(-8.75, 5, -15), texture='purg_wall', color=color.white, collider="box")'''
    #print(scaler(map_string, 2))
    f = open("output.txt", "w")
    f.write(scale_height(map_string, 10))
    f.close()
