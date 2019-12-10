from dependency_injector import providers, containers
from LumiduinoNodePython.tcpserver import TcpServer
from LumiduinoNodePython.tcpclient import TcpClient
from LumiduinoNodePython.customlogger import CustomLogger
from LumiduinoNodePython.arduino_firmata import FirmataArduino
from LumiduinoNodePython.node_broadcaster import NodeInformationBroadcaster
class LumiduinoServer(containers.DeclarativeContainer):

    config = providers.Configuration('config')
    
    logger = providers.Singleton(CustomLogger,
        file_path=config.logging.file_path,
        verbose=config.logging.verbose
    )

    arduino_service = providers.Singleton(FirmataArduino,
        port=config.arduino.location,
        logger=logger
    )

    broadcaster = providers.Singleton(
        NodeInformationBroadcaster,
        serverport=config.server.port,
        logger=logger,
        arduino=arduino_service
    )

    lumiduino_tcp_server = providers.Singleton(
        TcpServer,
        port=config.server.port,
        logger=logger,
    )

class LumiduinoClient(containers.DeclarativeContainer):
    tcp_client = providers.Factory(
        TcpClient,
        arduino_service=LumiduinoServer.arduino_service,
        logger=LumiduinoServer.logger)

