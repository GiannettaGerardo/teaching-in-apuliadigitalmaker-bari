package its.bari.resourceserver.controller;

import its.bari.resourceserver.model.MyModel;
import its.bari.resourceserver.service.MyService;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("api/v1")
public class Controller {
    private final MyService myService;

    public Controller(MyService myService) {
        this.myService = myService;
    }

    @GetMapping("/")
    public MyModel getMyModel() {
        return myService.getMyModel();
    }

}
