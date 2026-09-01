package cn.edu.hdu.packing_service.service.Impl;

import cn.edu.hdu.packing_service.mapper.SpecificationMapper;
import cn.edu.hdu.packing_service.pojo.*;
import cn.edu.hdu.packing_service.pojo.dto.PalletRollDTO;
import cn.edu.hdu.packing_service.service.SpecificationService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.sql.SQLIntegrityConstraintViolationException;
import java.util.Collections;
import java.util.List;
import java.util.Map;

/**
 * @Author: ZhangWH
 * @Date: 2024/3/18 11:07
 */
@Service
public class SpecificationServiceImp implements SpecificationService {


    @Autowired
    SpecificationMapper specificationMapper;

    @Override
    public List<PalletSpecification> queryAllPallet() {
        return specificationMapper.queryAllPallet();
    }

    @Override
    public void updatePallet(PalletSpecification palletSpecification) {
        specificationMapper.updatePallet(palletSpecification);
    }

    @Override
    public void addPallet(PalletSpecification palletSpecification) {
        specificationMapper.addPallet(palletSpecification);
    }

    @Override
    public void deletePallet(Integer id) {
        specificationMapper.deletePallet(id);
    }

    @Override
    public List<TruckSpecification> queryAllTruck() {
        return specificationMapper.queryAllTruck();
    }

    @Override
    public void addTruck(TruckSpecification truckSpecification) {
        specificationMapper.addTruck(truckSpecification);
    }

    @Override
    public void updateTruck(TruckSpecification truckSpecification) {
        specificationMapper.updateTruck(truckSpecification);
    }

    @Override
    public void deleteTruck(Integer id) {
        specificationMapper.deleteTruck(id);
    }

    @Override
    public Map<String , Object> queryAllSpecification() {
        Map<String , Object> res = new java.util.HashMap<>();
        res.put("pallet", specificationMapper.queryAllPallet());
        res.put("truck", specificationMapper.queryAllTruck());
        return res;
    }

    @Override
    public List<RollSpecification> queryAllRoll() {
        return specificationMapper.queryAllRoll();
    }

    @Override
    public Integer addRoll(RollSpecification rollSpecification) {
        specificationMapper.addRoll(rollSpecification);
        return rollSpecification.getId();
    }

    @Override
    public void updateRoll(RollSpecification rollSpecification) {
        specificationMapper.updateRoll(rollSpecification);
    }

    @Override
    public void deleteRoll(Integer id) {
        specificationMapper.deleteRoll(id);
    }

    @Override
    public List<PalletRollRelations> queryAllpalletroll() {
        return specificationMapper.queryAllPalletRollRelations();
    }

    @Override
    public void updatePalletRoll(PalletRollRelations palletRollRelations) {
        specificationMapper.updatePalletRoll(palletRollRelations);
    }

    @Override
    public void addPalletRoll(PalletRollRelations palletRollRelations) {
        specificationMapper.addPalletRoll(palletRollRelations);
    }

    @Override
    public void deletePalletRoll(Integer palletId, Integer rollId) {
        specificationMapper.deletePalletRoll(palletId, rollId);
    }

    @Override
    public List<PalletRollDTO> queryByPalletId(Integer palletId) {
        return specificationMapper.queryByPalletId(palletId);
    }

    @Override
    public List<PalletRollDTO> queryByRollId(Integer rollId) {
        return specificationMapper.queryByRollId(rollId);
    }

    @Override
    public PalletSpecification queryPalletById(Integer palletId) {
        return specificationMapper.queryPalletById(palletId);
    }

    @Override
    public List<TubeSpecification> queryAllTube() {
        return specificationMapper.queryAllTube();
    }

    @Override
    public void addTube(TubeSpecification tubeSpecification) {
        specificationMapper.addTube(tubeSpecification);
    }

    @Override
    public void updateTube(TubeSpecification tubeSpecification) {
        specificationMapper.updateTube(tubeSpecification);
    }

    @Override
    public void deleteTube(Integer id) {
        specificationMapper.deleteTube(id);
    }

}
