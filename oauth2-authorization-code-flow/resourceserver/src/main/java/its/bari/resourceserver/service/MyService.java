package its.bari.resourceserver.service;

import its.bari.resourceserver.model.MyModel;
import its.bari.resourceserver.repository.MyRepository;
import its.bari.resourceserver.repository.MyRepositoryImpl;
import org.springframework.stereotype.Service;

@Service
public class MyService {
    private final MyRepository myRepository;

    public MyService() {
        this.myRepository = new MyRepositoryImpl();
    }

    public MyModel getMyModel() {
        return myRepository.getMyModel();
    }
}
