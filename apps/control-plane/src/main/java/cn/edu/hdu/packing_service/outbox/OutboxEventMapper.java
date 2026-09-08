package cn.edu.hdu.packing_service.outbox;

import org.apache.ibatis.annotations.Insert;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Options;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;
import org.apache.ibatis.annotations.Update;

import java.time.LocalDateTime;
import java.util.List;

@Mapper
public interface OutboxEventMapper {

    @Insert("insert into packing_outbox_event " +
            "(event_id, deduplication_key, aggregate_type, aggregate_id, event_type, user_id, trace_id, " +
            "payload_json, status, attempt, max_attempts, available_at, created_at, updated_at, version) values " +
            "(#{eventId}, #{deduplicationKey}, #{aggregateType}, #{aggregateId}, #{eventType}, #{userId}, " +
            "#{traceId}, #{payloadJson}, #{status}, #{attempt}, #{maxAttempts}, #{availableAt}, #{createdAt}, " +
            "#{updatedAt}, #{version}) on duplicate key update id = last_insert_id(id), updated_at = updated_at")
    @Options(useGeneratedKeys = true, keyProperty = "id", keyColumn = "id")
    int insertIdempotent(OutboxEvent event);

    @Select("select * from packing_outbox_event where id = #{id}")
    OutboxEvent findById(Long id);

    @Select("select * from packing_outbox_event where deduplication_key = #{deduplicationKey}")
    OutboxEvent findByDeduplicationKey(String deduplicationKey);

    @Select("select * from packing_outbox_event " +
            "where status = 'PENDING' and available_at <= #{now} and attempt < max_attempts " +
            "order by status asc, available_at asc, created_at asc, id asc " +
            "limit 1 for update skip locked")
    OutboxEvent lockNextPublishable(@Param("now") LocalDateTime now);

    @Select("select * from packing_outbox_event where event_id = #{eventId} for update")
    OutboxEvent lockByEventId(@Param("eventId") String eventId);

    @Select("select * from packing_outbox_event " +
            "where status = 'PUBLISHING' and lease_expires_at <= #{now} " +
            "order by lease_expires_at asc, id asc limit #{limit} for update skip locked")
    List<OutboxEvent> lockExpiredLeases(@Param("now") LocalDateTime now,
                                         @Param("limit") int limit);

    @Update("update packing_outbox_event set status = 'PUBLISHING', attempt = attempt + 1, " +
            "lease_owner = #{leaseOwner}, lease_token = #{leaseToken}, lease_expires_at = #{leaseExpiresAt}, " +
            "updated_at = #{now}, version = version + 1 " +
            "where id = #{id} and version = #{version} and status = 'PENDING' and available_at <= #{now}")
    int claim(@Param("id") Long id,
              @Param("version") Integer version,
              @Param("leaseOwner") String leaseOwner,
              @Param("leaseToken") String leaseToken,
              @Param("leaseExpiresAt") LocalDateTime leaseExpiresAt,
              @Param("now") LocalDateTime now);

    @Update("update packing_outbox_event set status = 'PUBLISHED', lease_owner = null, lease_token = null, " +
            "lease_expires_at = null, last_error = null, published_at = #{now}, updated_at = #{now}, " +
            "version = version + 1 where id = #{id} and version = #{version} and status = 'PUBLISHING' " +
            "and lease_token = #{leaseToken}")
    int markPublished(@Param("id") Long id,
                      @Param("version") Integer version,
                      @Param("leaseToken") String leaseToken,
                      @Param("now") LocalDateTime now);

    @Update("update packing_outbox_event set status = 'PENDING', available_at = #{availableAt}, " +
            "lease_owner = null, lease_token = null, lease_expires_at = null, last_error = #{lastError}, " +
            "updated_at = #{now}, version = version + 1 " +
            "where id = #{id} and version = #{version} and status = 'PUBLISHING' and lease_token = #{leaseToken}")
    int retry(@Param("id") Long id,
              @Param("version") Integer version,
              @Param("leaseToken") String leaseToken,
              @Param("availableAt") LocalDateTime availableAt,
              @Param("lastError") String lastError,
              @Param("now") LocalDateTime now);

    @Update("update packing_outbox_event set status = 'DEAD_LETTER', lease_owner = null, lease_token = null, " +
            "lease_expires_at = null, last_error = #{lastError}, updated_at = #{now}, version = version + 1 " +
            "where id = #{id} and version = #{version} and status = 'PUBLISHING' and lease_token = #{leaseToken}")
    int deadLetter(@Param("id") Long id,
                   @Param("version") Integer version,
                   @Param("leaseToken") String leaseToken,
                   @Param("lastError") String lastError,
                   @Param("now") LocalDateTime now);

    @Update("update packing_outbox_event set status = 'PENDING', available_at = #{availableAt}, " +
            "lease_owner = null, lease_token = null, lease_expires_at = null, last_error = #{lastError}, " +
            "updated_at = #{now}, version = version + 1 " +
            "where id = #{id} and version = #{version} and status = 'PUBLISHING'")
    int recoverExpired(@Param("id") Long id,
                       @Param("version") Integer version,
                       @Param("availableAt") LocalDateTime availableAt,
                       @Param("lastError") String lastError,
                       @Param("now") LocalDateTime now);

    @Update("update packing_outbox_event set status = 'DEAD_LETTER', lease_owner = null, lease_token = null, " +
            "lease_expires_at = null, last_error = #{lastError}, updated_at = #{now}, version = version + 1 " +
            "where id = #{id} and version = #{version} and status = 'PUBLISHING'")
    int deadLetterExpired(@Param("id") Long id,
                          @Param("version") Integer version,
                          @Param("lastError") String lastError,
                          @Param("now") LocalDateTime now);

    @Select("select status, count(*) as count from packing_outbox_event group by status")
    List<OutboxStatusCount> countByStatus();

    @Select("select * from packing_outbox_event where user_id = #{userId} and id > #{afterId} " +
            "order by id asc limit #{limit}")
    List<OutboxEvent> listForUserAfter(@Param("userId") String userId,
                                       @Param("afterId") long afterId,
                                       @Param("limit") int limit);
}
