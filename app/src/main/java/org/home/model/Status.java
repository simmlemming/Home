package org.home.model;

import java.util.List;

/**
 * Created by mtkachenko on 20/12/15.
 */
public class Status {
    public int time;
    public String state;
    public List<Sensor> sensors;

    public static class Sensor {
        public String name;
        public int state;
    }
}
