package cn.edu.hdu.packing_service.job;

import org.apache.ibatis.annotations.Insert;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;
import org.apache.ibatis.annotations.Update;

import java.time.LocalDateTime;
import java.util.List;

@Mapper
public interface PackingJobMapper {

    @Insert("insert into packing_job " +
            "(public_id, task_id, job_type, status, payload_json, priority, attempt, max_attempts, " +
            "available_at, idempotency_key, created_at, updated_at, version) values " +
            "(#{publicId}, #{taskId}, #{jobType}, #{status}, #{payloadJson}, #{priority}, #{attempt}, " +
            "#{maxAttempts}, #{availableAt}, #{idempotencyKey}, #{createdAt}, #{updatedAt}, #{version}) " +
            "on duplicate key update id = last_insert_id(id), updated_at = updated_at")
    @org.apache.ibatis.annotations.Options(useGeneratedKeys = true, keyProperty = "id", keyColumn = "id")
    void insertIdempotent(PackingJob job);

    @Select("select * from packing_job where id = #{id}")
    PackingJob findById(Long id);

    @Select("select * from packing_job where public_id = #{publicId}")
    PackingJob findByPublicId(String publicId);

    @Select("select * from packing_job where task_id = #{taskId} order by created_at desc limit 1")
    PackingJob findLatestByTaskId(Integer taskId);

    PackingJob lockNextClaimable(@Param("jobTypes") List<String> jobTypes,
                                 @Param("now") LocalDateTime now);

    PackingJob lockByPublicId(@Param("publicId") String publicId);

    List<PackingJob> lockExpiredLeases(@Param("now") LocalDateTime now,
                                       @Param("limit") int limit);

    @Update("update packing_job set status = 'RUNNING', attempt = attempt + 1, " +
            "lease_owner = #{workerId}, lease_token = #{leaseToken}, lease_expires_at = #{leaseExpiresAt}, " +
            "heartbeat_at = #{now}, started_at = coalesce(started_at, #{now}), updated_at = #{now}, version = version + 1 " +
            "where id = #{id} and version = #{version} and status in ('QUEUED', 'RETRY_WAIT')")
    int claim(@Param("id") Long id,
              @Param("version") Integer version,
              @Param("workerId") String workerId,
              @Param("leaseToken") String leaseToken,
              @Param("leaseExpiresAt") LocalDateTime leaseExpiresAt,
              @Param("now") LocalDateTime now);

    @Update("update packing_job set lease_expires_at = #{leaseExpiresAt}, heartbeat_at = #{now}, " +
            "updated_at = #{now}, version = version + 1 where public_id = #{publicId} " +
            "and status = 'RUNNING' and lease_token = #{leaseToken} and lease_expires_at > #{now}")
    int heartbeat(@Param("publicId") String publicId,
                  @Param("leaseToken") String leaseToken,
                  @Param("leaseExpiresAt") LocalDateTime leaseExpiresAt,
                  @Param("now") LocalDateTime now);

    @Update("update packing_job set status = 'SUCCEEDED', result_json = #{resultJson}, " +
            "lease_owner = null, lease_token = null, lease_expires_at = null, heartbeat_at = #{now}, " +
            "finished_at = #{now}, updated_at = #{now}, version = version + 1 " +
            "where id = #{id} and version = #{version} and status = 'RUNNING' and lease_token = #{leaseToken}")
    int succeed(@Param("id") Long id,
                @Param("version") Integer version,
                @Param("leaseToken") String leaseToken,
                @Param("resultJson") String resultJson,
                @Param("now") LocalDateTime now);

    @Update("update packing_job set status = 'RETRY_WAIT', available_at = #{availableAt}, " +
            "lease_owner = null, lease_token = null, lease_expires_at = null, error_code = #{errorCode}, " +
            "error_message = #{errorMessage}, updated_at = #{now}, version = version + 1 " +
            "where id = #{id} and version = #{version} and status = 'RUNNING'")
    int retry(@Param("id") Long id,
              @Param("version") Integer version,
              @Param("availableAt") LocalDateTime availableAt,
              @Param("errorCode") String errorCode,
              @Param("errorMessage") String errorMessage,
              @Param("now") LocalDateTime now);

    @Update("update packing_job set status = 'DEAD_LETTER', lease_owner = null, lease_token = null, " +
            "lease_expires_at = null, error_code = #{errorCode}, error_message = #{errorMessage}, " +
            "finished_at = #{now}, updated_at = #{now}, version = version + 1 " +
            "where id = #{id} and version = #{version} and status = 'RUNNING'")
    int deadLetter(@Param("id") Long id,
                   @Param("version") Integer version,
                   @Param("errorCode") String errorCode,
                   @Param("errorMessage") String errorMessage,
                   @Param("now") LocalDateTime now);
}
