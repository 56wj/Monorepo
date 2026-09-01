package cn.edu.hdu.packing_service.mapper;

import cn.edu.hdu.packing_service.pojo.*;
import cn.edu.hdu.packing_service.pojo.dto.PalletRollDTO;
import org.apache.ibatis.annotations.*;

import java.util.List;

/**
 * @Author: ZhangWH
 * @Date: 2024/3/18 11:07
 */
@Mapper
public interface SpecificationMapper {

    @Select("select * from spe_pallet")
    List<PalletSpecification> queryAllPallet();

    @Update("update spe_pallet set pallet_name = #{palletName}, pallet_length = #{palletLength}, pallet_width = #{palletWidth}, pallet_height = #{palletHeight}," +
            " pallet_weight = #{palletWeight}, pallet_type = #{palletType} ,pallet_remark = #{palletRemark} where id = #{id}")
    void updatePallet(PalletSpecification palletSpecification);

    @Insert("INSERT INTO spe_pallet (pallet_name, pallet_length, pallet_width, pallet_height, pallet_weight , pallet_type , pallet_remark) " +
            "VALUES ( #{palletName}, #{palletLength}, #{palletWidth}, #{palletHeight}, #{palletWeight} , #{palletType} ,#{palletRemark})")
    void addPallet(PalletSpecification palletSpecification);

    @Delete("delete from spe_pallet where id = #{id}")
    void deletePallet(Integer id);


    @Select("select * from spe_truck")
    List<TruckSpecification> queryAllTruck();

    @Update("update spe_truck set name = #{name}, length_m = #{lengthM}, width_m = #{widthM}, height_m = #{heightM}, weight_t = #{weightT} where id = #{id}")
    void updateTruck(TruckSpecification truckSpecification);

    @Insert("INSERT INTO spe_truck (name, length_m, width_m, height_m, weight_t) " +
            "VALUES ( #{name}, #{lengthM}, #{widthM}, #{heightM}, #{weightT})")
    void addTruck(TruckSpecification truckSpecification);

    @Delete("delete from spe_truck where id = #{id}")
    void deleteTruck(Integer id);

    @Select("select * from spe_roll")
    List<RollSpecification> queryAllRoll();

    @Insert("INSERT INTO spe_roll (roll_name, roll_thickness, roll_length) " +
            "VALUES ( #{rollName}, #{rollThickness}, #{rollLength})")
    @Options(useGeneratedKeys = true, keyProperty = "id")  // 获取自动生成的主键
    void addRoll(RollSpecification rollSpecification);

    @Update("update spe_roll set roll_name = #{rollName}, roll_thickness = #{rollThickness}, roll_length = #{rollLength} where id = #{id}")
    void updateRoll(RollSpecification rollSpecification);

    @Delete("delete from spe_roll where id = #{id}")
    void deleteRoll(Integer id);

    @Select("select * from spe_pallet_roll_relations")
    List<PalletRollRelations> queryAllPalletRollRelations();

    @Update("update spe_pallet_roll_relations set roll_nums = #{rollNums} where pallet_id = #{palletId} and roll_id = #{rollId} ")
    void updatePalletRoll(PalletRollRelations palletRollRelations);

    @Delete("delete from spe_pallet_roll_relations where pallet_id = #{palletId} and roll_id = #{rollId}")
    void deletePalletRoll(Integer palletId, Integer rollId);

    @Insert("INSERT INTO spe_pallet_roll_relations (pallet_id, roll_id, roll_nums) " +
            "VALUES ( #{palletId}, #{rollId}, #{rollNums})")
    void addPalletRoll(PalletRollRelations palletRollRelations);

    @Select("SELECT *\n" +
            "FROM spe_pallet as p\n" +
            "JOIN spe_pallet_roll_relations prr ON p.id = prr.pallet_id\n" +
            "JOIN spe_roll r ON prr.roll_id = r.id\n" +
            "WHERE p.id = #{palletId};\n")
    List<PalletRollDTO> queryByPalletId(Integer palletId);

    @Select("SELECT *\n" +
            "FROM spe_pallet as p\n" +
            "JOIN spe_pallet_roll_relations prr ON p.id = prr.pallet_id\n" +
            "JOIN spe_roll r ON prr.roll_id = r.id\n" +
            "WHERE r.id = #{rollId};\n")
    List<PalletRollDTO> queryByRollId(Integer rollId);

    @Select("select * from spe_pallet where id = #{palletId}")
    PalletSpecification queryPalletById(Integer palletId);

    @Select("select * from spe_tube")
    List<TubeSpecification> queryAllTube();

    @Insert("INSERT INTO spe_tube (tube_name, tube_approximate) " +
            "VALUES ( #{tubeName}, #{tubeApproximate})")
    void addTube(TubeSpecification tubeSpecification);

    @Update("update spe_tube set tube_name = #{tubeName}, tube_approximate = #{tubeApproximate} where id = #{id}")
    void updateTube(TubeSpecification tubeSpecification);

    @Delete("delete from spe_tube where id = #{id}")
    void deleteTube(Integer id);
}
