package cn.edu.hdu.packing_service.service;

import cn.edu.hdu.packing_service.pojo.*;
import cn.edu.hdu.packing_service.pojo.dto.PalletRollDTO;

import java.util.List;
import java.util.Map;

/**
 * @Author: ZhangWH
 * @Date: 2024/3/18 11:06
 */
public interface SpecificationService {

    //查询所有规格
    public List<PalletSpecification> queryAllPallet();

    //修改规格
    void updatePallet(PalletSpecification palletSpecification);

    //新增规格
    void addPallet(PalletSpecification palletSpecification);

    //删除规格
    void deletePallet(Integer id);

    //查询所有车辆规格
    List<TruckSpecification> queryAllTruck();

    //添加车辆规格
    void addTruck(TruckSpecification truckSpecification);

    //修改车辆规格
    void updateTruck(TruckSpecification truckSpecification);

    //删除车辆规格
    void deleteTruck(Integer id);

    //查询所有规格
    Map<String , Object> queryAllSpecification();

    //查询所有卷规格
    List<RollSpecification> queryAllRoll();

    //添加卷规格
    Integer addRoll(RollSpecification rollSpecification);

    //修改卷规格
    void updateRoll(RollSpecification rollSpecification);

    //删除卷规格
    void deleteRoll(Integer id);

    //查询所有托盘卷规格
    List<PalletRollRelations> queryAllpalletroll();

    //修改托盘卷规格
    void updatePalletRoll(PalletRollRelations palletRollRelations);

    //添加托盘卷规格
    void addPalletRoll(PalletRollRelations palletRollRelations);

    //删除托盘卷规格
    void deletePalletRoll(Integer palletId, Integer rollId);

    //根据托盘id查询卷规格
    List<PalletRollDTO> queryByPalletId(Integer palletId);

    //根据卷id查询托盘规格
    List<PalletRollDTO> queryByRollId(Integer rollId);

    //根据托盘id查询规格
    PalletSpecification queryPalletById(Integer palletId);

    //查询所有纸管规格
    List<TubeSpecification> queryAllTube();

    //添加纸管规格
    void addTube(TubeSpecification tubeSpecification);

    //修改纸管规格
    void updateTube(TubeSpecification tubeSpecification);

    //删除纸管规格
    void deleteTube(Integer id);
}
