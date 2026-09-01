package cn.edu.hdu.packing_service.controller;

import cn.edu.hdu.packing_service.pojo.*;
import cn.edu.hdu.packing_service.pojo.dto.PalletRollDTO;
import cn.edu.hdu.packing_service.service.SpecificationService;
import cn.edu.hdu.packing_service.service.UserService;
import cn.edu.hdu.packing_service.utils.ThreadLocalUtil;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

/**
 * @Author: ZhangWH
 * @Date: 2024/3/18 11:06
 */
@RestController
@RequestMapping("/specification")
public class SpecificationController {

    @Autowired
    SpecificationService specificationService;

    @Autowired
    UserService userService;

    private final Lock rollLock = new ReentrantLock();

    private final Object lock = new Object();


    //查询托盘所有规格
    @RequestMapping("/pallet/queryAll")
    public Result queryAllPallet() {
        List<PalletSpecification> palletSpecificationList = specificationService.queryAllPallet();
        return Result.success(palletSpecificationList);
    }

    //修改托盘规格
    @PostMapping("/pallet/update")
    public Result updatePallet(@RequestBody @Validated(PalletSpecification.Update.class) PalletSpecification palletSpecification) {
        //获取当前用户id
        Map<String , Object> claims = ThreadLocalUtil.get();
        Integer userId = (Integer) claims.get("id");
        //验证用户权限
        Boolean hasPermission = userService.hasPermission(userId);

        if (!hasPermission) {
            return Result.error("没有权限");
        }

        //判断是否已存在该规格
        List<PalletSpecification> palletSpecificationList = specificationService.queryAllPallet();
        for (PalletSpecification tmp : palletSpecificationList) {
            if (tmp.equals(palletSpecification) && !tmp.getId().equals(palletSpecification.getId())){
                return Result.error("规格已存在");
            }
        }

        specificationService.updatePallet(palletSpecification);
        return Result.success();
    }

    //新增托盘规格
    @PutMapping("/pallet/add")
    public Result addPallet(@RequestBody @Validated(PalletSpecification.Add.class) PalletSpecification palletSpecification) {
        //获取当前用户id
        Map<String , Object> claims = ThreadLocalUtil.get();
        Integer userId = (Integer) claims.get("id");
        //验证用户权限
        Boolean hasPermission = userService.hasPermission(userId);

        if (!hasPermission) {
            return Result.error("没有权限");
        }

        //判断是否已存在该规格
        List<PalletSpecification> palletSpecificationList = specificationService.queryAllPallet();
        for (PalletSpecification tmp : palletSpecificationList) {
            if (tmp.equals(palletSpecification)) {
                return Result.error("规格已存在");
            }
        }

        specificationService.addPallet(palletSpecification);
        return Result.success();
    }

    //删除托盘规格
    @DeleteMapping("/pallet/delete")
    public Result deletePallet(Integer id) {
        //获取当前用户id
        Map<String , Object> claims = ThreadLocalUtil.get();
        Integer userId = (Integer) claims.get("id");
        //验证用户权限
        Boolean hasPermission = userService.hasPermission(userId);

        if (!hasPermission) {
            return Result.error("没有权限");
        }
        specificationService.deletePallet(id);
        return Result.success();
    }

    //查询货车所有规格
    @RequestMapping("/truck/queryAll")
    public Result queryAllTruck() {
        List<TruckSpecification> truckSpecificationList = specificationService.queryAllTruck();
        return Result.success(truckSpecificationList);
    }

    //新增货车规格
    @PutMapping("/truck/add")
    public Result addTruck(@RequestBody @Validated(TruckSpecification.Add.class) TruckSpecification truckSpecification) {
        //获取当前用户id
        Map<String , Object> claims = ThreadLocalUtil.get();
        Integer userId = (Integer) claims.get("id");
        //验证用户权限
        Boolean hasPermission = userService.hasPermission(userId);

        if (!hasPermission) {
            return Result.error("没有权限");
        }

        //判断是否已存在该规格
        List<TruckSpecification> truckSpecificationList = specificationService.queryAllTruck();
        for (TruckSpecification truckSpecificationTmp : truckSpecificationList) {
            if (truckSpecification.getLengthM() == truckSpecificationTmp.getLengthM() &&
                    truckSpecification.getWidthM() == truckSpecificationTmp.getWidthM() &&
                    truckSpecification.getHeightM() == truckSpecificationTmp.getHeightM() &&
                    truckSpecification.getWeightT() == truckSpecificationTmp.getWeightT() &&
                    !truckSpecification.getId().equals(truckSpecificationTmp.getId())
            ) {

                return Result.error("已存在该规格");
            }
            if (truckSpecification.getName().equals(truckSpecificationTmp.getName())) {
                return Result.error("已存在车辆名称");
            }
        }

        specificationService.addTruck(truckSpecification);
        return Result.success();
    }

    //修改货车规格
    @PostMapping("/truck/update")
    public Result updateTruck(@RequestBody @Validated(TruckSpecification.Update.class) TruckSpecification truckSpecification) {

        //获取当前用户id
        Map<String , Object> claims = ThreadLocalUtil.get();
        Integer userId = (Integer) claims.get("id");
        //验证用户权限
        Boolean hasPermission = userService.hasPermission(userId);

        if (!hasPermission) {
            return Result.error("没有权限");
        }

        //判断是否已存在该规格
        List<TruckSpecification> truckSpecificationList = specificationService.queryAllTruck();
        for (TruckSpecification truckSpecificationTmp : truckSpecificationList) {
            if (truckSpecification.getLengthM().equals( truckSpecificationTmp.getLengthM()) &&
                    truckSpecification.getWidthM().equals( truckSpecificationTmp.getWidthM()) &&
                    truckSpecification.getHeightM().equals(truckSpecificationTmp.getHeightM()) &&
                    truckSpecification.getWeightT().equals(truckSpecificationTmp.getWeightT()) &&
                    !truckSpecification.getId().equals(truckSpecificationTmp.getId())) {

                return Result.error("已存在该规格");
            }
            if (truckSpecification.getName().equals(truckSpecificationTmp.getName()) && !truckSpecification.getId().equals(truckSpecificationTmp.getId())) {
                return Result.error("已存在车辆名称");
            }
        }

        specificationService.updateTruck(truckSpecification);
        return Result.success();
    }

    //删除货车规格
    @DeleteMapping("/truck/delete")
    public Result deleteTruck(Integer id) {
        //获取当前用户id
        Map<String , Object> claims = ThreadLocalUtil.get();
        Integer userId = (Integer) claims.get("id");
        //验证用户权限
        Boolean hasPermission = userService.hasPermission(userId);

        if (!hasPermission) {
            return Result.error("没有权限");
        }
        specificationService.deleteTruck(id);
        return Result.success();
    }

    //查询卷膜规格
    @RequestMapping("/roll/queryAll")
    public Result queryAllRoll() {
        List<RollSpecification> rollSpecificationList = specificationService.queryAllRoll();
        return Result.success(rollSpecificationList);
    }

    //新增卷膜规格
    @PutMapping("/roll/add")
    public Result addRoll(@RequestBody @Validated(RollSpecification.Add.class) RollSpecification rollSpecification) {
        //获取当前用户id
        Map<String , Object> claims = ThreadLocalUtil.get();
        Integer userId = (Integer) claims.get("id");
        //验证用户权限
        Boolean hasPermission = userService.hasPermission(userId);

        if (!hasPermission) {
            return Result.error("没有权限");
        }

        //判断是否已存在该规格
        List<RollSpecification> rollSpecificationList = specificationService.queryAllRoll();
        for (RollSpecification rollSpecificationTmp : rollSpecificationList) {
            if (rollSpecificationTmp.equals(rollSpecification)
            ) {

                return Result.error("已存在该规格");
            }
        }

        specificationService.addRoll(rollSpecification);
        return Result.success();
    }





    //修改卷膜规格
    @PostMapping("/roll/update")
    public Result updateRoll(@RequestBody @Validated(RollSpecification.Update.class) RollSpecification rollSpecification) {
        //获取当前用户id
        Map<String , Object> claims = ThreadLocalUtil.get();
        Integer userId = (Integer) claims.get("id");
        //验证用户权限
        Boolean hasPermission = userService.hasPermission(userId);

        if (!hasPermission) {
            return Result.error("没有权限");
        }

        //判断是否已存在该规格
        List<RollSpecification> rollSpecificationList = specificationService.queryAllRoll();
        for (RollSpecification rollSpecificationTmp : rollSpecificationList) {
            if (rollSpecificationTmp.equals(rollSpecification) && !rollSpecificationTmp.getId().equals(rollSpecification.getId())) {
                return Result.error("已存在该规格");
            }
        }

        specificationService.updateRoll(rollSpecification);
        return Result.success();
    }

    //删除卷膜规格
    @DeleteMapping("/roll/delete")
    public Result deleteRoll(Integer id) {
        //获取当前用户id
        Map<String , Object> claims = ThreadLocalUtil.get();
        Integer userId = (Integer) claims.get("id");
        //验证用户权限
        Boolean hasPermission = userService.hasPermission(userId);

        if (!hasPermission) {
            return Result.error("没有权限");
        }
        specificationService.deleteRoll(id);
        return Result.success();
    }


    //查询卷数规格
    @RequestMapping("/palletroll/queryAll")
    public Result queryAllRollNum() {
        List<PalletRollRelations> palletrollList = specificationService.queryAllpalletroll();
        return Result.success(palletrollList);
    }

    //添加卷数规格
    @PutMapping("/palletroll/add")
    public Result addRollNum(@RequestBody @Validated(PalletRollRelations.Add.class) PalletRollRelations palletRollRelations) {
        //获取当前用户id
        Map<String , Object> claims = ThreadLocalUtil.get();
        Integer userId = (Integer) claims.get("id");
        //验证用户权限
        Boolean hasPermission = userService.hasPermission(userId);

        if (!hasPermission) {
            return Result.error("没有权限");
        }

        //判断是否已存在该规格
        List<PalletRollRelations> palletrollList = specificationService.queryAllpalletroll();
        for (PalletRollRelations palletrollTmp : palletrollList) {
            if (palletrollTmp.equals(palletRollRelations)) {
                return Result.error("已存在该规格");
            }
        }
        specificationService.addPalletRoll(palletRollRelations);

        return Result.success();
    }


    //无权限创建卷数规格
    @PutMapping("/palletroll/create")
    public Result createRollNum(@RequestBody Map<String, Object> data) {
        //判断添加数是否为0
        if ((Integer) data.get("rollNums") == 0) {
            return Result.error("添加数不能为0");
        }

        Integer rollId = null;

        //判断卷膜规格是否存在
        rollLock.lock(); // 获取锁
        try {
            List<RollSpecification> rollSpecificationList = specificationService.queryAllRoll();
            Boolean flag = false;
            for (RollSpecification rollSpecification : rollSpecificationList) {
                if (Double.compare(rollSpecification.getRollLength(), Double.parseDouble((String) data.get("rollLength"))) == 0 &&
                        Double.compare(rollSpecification.getRollThickness(), Double.parseDouble((String) data.get("rollThickness"))) == 0 &&
                        rollSpecification.getRollName().equals(data.get("rollName"))) {
                    flag = true;
                    rollId = rollSpecification.getId();
                    System.out.println("卷膜规格已存在");
                    break;
                }
            }


            if (!flag) {        //不存在则添加卷膜，并赋值给卷膜ID
                System.out.println("卷膜规格不存在");
                RollSpecification rollSpecification = new RollSpecification();
                rollSpecification.setRollName((String) data.get("rollName"));
                rollSpecification.setRollLength(Double.valueOf((String) data.get("rollLength")));
                rollSpecification.setRollThickness(Double.valueOf((String) data.get("rollThickness")));
                rollId = specificationService.addRoll(rollSpecification);

            }




            //判断是否已存在该规格
            List<PalletRollRelations> palletrollList = specificationService.queryAllpalletroll();
            for (PalletRollRelations palletrollTmp : palletrollList) {
                if (palletrollTmp.getPalletId().equals(data.get("palletId")) && palletrollTmp.getRollId().equals(rollId)) {
                    return Result.success("卷数已存在该规格");
                }
            }

            //添加卷数规格
            PalletRollRelations palletRollRelations = new PalletRollRelations();
            palletRollRelations.setPalletId((Integer) data.get("palletId"));
            palletRollRelations.setRollId(rollId);
            palletRollRelations.setRollNums((Integer) data.get("rollNums"));
            specificationService.addPalletRoll(palletRollRelations);
        }finally {
            rollLock.unlock(); // 释放锁
        }
        return Result.success();
    }


    //修改卷数规格
    @PostMapping("/palletroll/update")
    public Result updateRollNum(@RequestBody @Validated(PalletRollRelations.Update.class) PalletRollRelations palletRollRelations) {
        //获取当前用户id
        Map<String , Object> claims = ThreadLocalUtil.get();
        Integer userId = (Integer) claims.get("id");
        //验证用户权限
        Boolean hasPermission = userService.hasPermission(userId);

        if (!hasPermission) {
            return Result.error("没有权限");
        }

        //判断添加数是否为0
        if (palletRollRelations.getRollNums() == 0) {
            return Result.error("添加数不能为0");
        }
        //判断是否已存在该规格
        List<PalletRollRelations> palletrollList = specificationService.queryAllpalletroll();
        for (PalletRollRelations palletrollTmp : palletrollList) {
            if (palletrollTmp.equals(palletRollRelations)) {
                specificationService.updatePalletRoll(palletRollRelations);
                return Result.success();
            }
        }

        //不存在则添加新的数据
        specificationService.addPalletRoll(palletRollRelations);
        return Result.success();
    }

    //删除卷数规格
    @DeleteMapping("/palletroll/delete")
    public Result deleteRollNum(Integer palletId, Integer rollId) {
        //获取当前用户id
        Map<String , Object> claims = ThreadLocalUtil.get();
        Integer userId = (Integer) claims.get("id");
        //验证用户权限
        Boolean hasPermission = userService.hasPermission(userId);

        if (!hasPermission) {
            return Result.error("没有权限");
        }

        specificationService.deletePalletRoll(palletId, rollId);

        return Result.success();
    }


    //查询所有规格
    @RequestMapping("/queryAll")
    public Result queryAllSpecification() {
        Map<String , Object> specificationList = specificationService.queryAllSpecification();
        return Result.success(specificationList);
    }


    //通过palletId查询卷数规格
    @RequestMapping("/palletroll/queryByPalletId")
    public Result queryByPalletId(Integer palletId) {
        List<PalletRollDTO> palletRollDTOList = specificationService.queryByPalletId(palletId);
        return Result.success(palletRollDTOList);
    }

    //通过rollId查询据卷数规格
    @RequestMapping("/palletroll/queryByRollId")
    public Result queryByRollId(Integer rollId) {
        List<PalletRollDTO> palletRollDTOList = specificationService.queryByRollId(rollId);

        //查询全部托盘规格
        List<PalletSpecification> palletSpecificationList = specificationService.queryAllPallet();

        //将不存在的托盘规格添加到返回结果中
        for (PalletSpecification palletSpecification : palletSpecificationList) {
            Boolean flag = false;
            for (PalletRollDTO palletRollDTO : palletRollDTOList) {
                if (palletRollDTO.getPalletId().equals(palletSpecification.getId())) {
                    flag = true;
                    break;
                }
            }
            if (!flag) {
                PalletRollDTO palletRollDTO = new PalletRollDTO();
                palletRollDTO.setPalletId(palletSpecification.getId());
                palletRollDTO.setPalletName(palletSpecification.getPalletName());
                palletRollDTO.setPalletLength(palletSpecification.getPalletLength());
                palletRollDTO.setPalletWidth(palletSpecification.getPalletWidth());
                palletRollDTO.setPalletHeight(palletSpecification.getPalletHeight());
                palletRollDTO.setPalletWeight(palletSpecification.getPalletWeight());
                palletRollDTO.setPalletType(palletSpecification.getPalletType());
                palletRollDTO.setPalletRemark(palletSpecification.getPalletRemark());
                palletRollDTO.setRollId(rollId);
                palletRollDTO.setRollNums(0);
                palletRollDTOList.add(palletRollDTO);
            }
        }

        return Result.success(palletRollDTOList);
    }


    //按照palletId查询托盘规格
    @RequestMapping("/pallet/queryById")
    public Result queryPalletById(Integer palletId) {
        PalletSpecification palletSpecification = specificationService.queryPalletById(palletId);
        return Result.success(palletSpecification);
    }

    //查询所有纸管规格
    @RequestMapping("/tube/queryAll")
    public Result queryAllTube() {
        List<TubeSpecification> tubeSpecificationList = specificationService.queryAllTube();
        return Result.success(tubeSpecificationList);
    }

    @RequestMapping("/tube/add")
    public Result addTube(@RequestBody TubeSpecification tubeSpecification) {
        //获取当前用户id
        Map<String , Object> claims = ThreadLocalUtil.get();
        Integer userId = (Integer) claims.get("id");
        //验证用户权限
        Boolean hasPermission = userService.hasPermission(userId);

        if (!hasPermission) {
            return Result.error("没有权限");
        }

        //判断是否已存在该规格
        List<TubeSpecification> tubeSpecificationList = specificationService.queryAllTube();
        for (TubeSpecification tubeSpecificationTmp : tubeSpecificationList) {
            if (tubeSpecificationTmp.equals(tubeSpecification)) {
                return Result.error("已存在该规格");
            }
        }

        //判断近似值是否为0
        if (tubeSpecification.getTubeApproximate() == 0) {
            return Result.error("近似值不能为0");
        }

        //添加纸管规格
        specificationService.addTube(tubeSpecification);
        return Result.success();
    }


    @RequestMapping("/tube/update")
    public Result updateTube(@RequestBody TubeSpecification tubeSpecification) {
        //获取当前用户id
        Map<String , Object> claims = ThreadLocalUtil.get();
        Integer userId = (Integer) claims.get("id");
        //验证用户权限
        Boolean hasPermission = userService.hasPermission(userId);

        if (!hasPermission) {
            return Result.error("没有权限");
        }

        //判断是否已存在该规格
        List<TubeSpecification> tubeSpecificationList = specificationService.queryAllTube();
        for (TubeSpecification tubeSpecificationTmp : tubeSpecificationList) {
            if (tubeSpecificationTmp.equals(tubeSpecification) && !tubeSpecificationTmp.getId().equals(tubeSpecification.getId())) {
                return Result.error("已存在该规格");
            }
        }

        //判断近似值是否为0
        if (tubeSpecification.getTubeApproximate() == 0) {
            return Result.error("近似值不能为0");
        }

        //修改纸管规格
        specificationService.updateTube(tubeSpecification);
        return Result.success();
    }


    //删除纸管规格
    @DeleteMapping("/tube/delete")
    public Result deleteTube(Integer id) {
        //获取当前用户id
        Map<String , Object> claims = ThreadLocalUtil.get();
        Integer userId = (Integer) claims.get("id");
        //验证用户权限
        Boolean hasPermission = userService.hasPermission(userId);

        if (!hasPermission) {
            return Result.error("没有权限");
        }

        specificationService.deleteTube(id);
        return Result.success();
    }


}
