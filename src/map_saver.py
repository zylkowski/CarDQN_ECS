import ecs
import ecs.exceptions
import data.components.segment as segment
import data.components.physics as physics
import data.components.car_control as car_control
from data.systems.entity_spawner_system import EntitySpawnerSystem
import jsonpickle
import data.constants
import pathlib


class MapSaver:

    @staticmethod
    def save_current_map(entity_manager: ecs.EntityManager):
        to_file = ""

        to_file = MapSaver.save_cars(entity_manager, to_file)
        to_file = MapSaver.save_segments(entity_manager, to_file)

        with open(MapSaver.unique_path(pathlib.Path.cwd(), 'map{:03}.txt'), 'w') as file:
            file.write(to_file)


    @staticmethod
    def save_segments(entity_manager, to_file):
        for segment_entity, segment_component in entity_manager.pairs_for_type(segment.SegmentComponent):
            try:
                seg_type: segment.SegmentTypeComponent = entity_manager \
                    .component_for_entity(segment_entity,
                                          segment.SegmentTypeComponent)

                if seg_type.type != segment.SegmentTypes.RAY:
                    seg_type_data = jsonpickle.encode(seg_type)
                    seg_component_data = jsonpickle.encode(segment_component)
                    to_file += f"S\n{seg_type_data}\n{seg_component_data}\n"
            except:
                pass
        return to_file

    @staticmethod
    def save_cars(entity_manager, to_file):
        for car_entity, _ in entity_manager.pairs_for_type(car_control.CarControllerComponent):
            try:
                position: physics.Position = entity_manager.component_for_entity(car_entity, physics.Position)
                rotation: physics.Rotation = entity_manager.component_for_entity(car_entity, physics.Rotation)

                position_data = jsonpickle.encode(position)
                rotation_data = jsonpickle.encode(rotation)
                to_file += f"C\n{position_data}\n{rotation_data}\n"
            except:
                pass
        return to_file

    @staticmethod
    def load_map(path):
        file = open(path,'r')
        while True:
            line =  file.readline()
            if not line:
                break

            line = line.strip()
            if line == "C":
                MapSaver.load_car(file)
            elif line == "S":
                MapSaver.load_segment(file)
            else:
                print("Unexpected line in map file")
        file.close()

    @staticmethod
    def load_segment(file):
        seg_type_data = file.readline()
        seg_component_data = file.readline()
        seg_type_component: segment.SegmentTypeComponent = jsonpickle.decode(seg_type_data)
        seg_component: segment.SegmentComponent = jsonpickle.decode(seg_component_data)

        EntitySpawnerSystem.spawn_segment(seg_type_component.type,
                                          seg_component.start,
                                          seg_component.end)

    @staticmethod
    def load_car(file):
        position_data = file.readline()
        rotation_data = file.readline()
        position_component = jsonpickle.decode(position_data)
        rotation_component = jsonpickle.decode(rotation_data)

        EntitySpawnerSystem.spawn_car_entity(position_component,
                                             rotation_component,
                                             data.constants.CAR_TEXTURE_PATH)

    @staticmethod
    def unique_path(directory, name_pattern):
        counter = 0
        while True:
            counter += 1
            path = directory / name_pattern.format(counter)
            if not path.exists():
                return path