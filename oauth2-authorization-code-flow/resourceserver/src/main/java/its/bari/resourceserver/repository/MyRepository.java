package its.bari.resourceserver.repository;

import its.bari.resourceserver.model.MyModel;
import org.springframework.stereotype.Component;

public interface MyRepository {
    MyModel getMyModel();
}
