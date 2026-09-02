# =====================================================
# Stage 1: Build - Maven 构建阶段
# =====================================================
FROM docker.m.daocloud.io/library/maven:3.8.6-openjdk-8 AS builder

WORKDIR /app

# 先复制 pom.xml，利用 Docker 层缓存下载依赖
COPY pom.xml .
RUN mvn dependency:go-offline -B

# 再复制源码进行构建
COPY src ./src
RUN mvn clean package -DskipTests -B

# =====================================================
# Stage 2: Runtime - 运行阶段（精简镜像）
# =====================================================
FROM docker.m.daocloud.io/library/eclipse-temurin:8-jre-jammy

WORKDIR /app

# 创建文件存储目录（替代 Windows 路径）
RUN mkdir -p /data/packing/source /data/packing/result /data/packing/middle /data/packing/push /data/packing/images /data/packing/logs

# 从构建阶段复制打包好的 JAR
COPY --from=builder /app/target/packing_service-0.0.2-SNAPSHOT.jar app.jar

# 暴露服务端口
EXPOSE 8101

# 启动时激活 docker profile
ENTRYPOINT ["java", "-Dspring.profiles.active=docker", "-jar", "app.jar"]
