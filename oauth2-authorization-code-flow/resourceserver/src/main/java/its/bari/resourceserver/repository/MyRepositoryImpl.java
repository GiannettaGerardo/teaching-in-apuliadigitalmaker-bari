package its.bari.resourceserver.repository;

import its.bari.resourceserver.model.MyModel;

public class MyRepositoryImpl implements MyRepository {
    @Override
    public MyModel getMyModel() {
        return new MyModel("ABCD1234", "This is my model");
    }
}
