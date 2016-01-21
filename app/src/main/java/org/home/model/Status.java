package org.home.model;

import java.util.List;

/**
 * Created by mtkachenko on 20/12/15.
 */
public class Status {
    public int time;
    /* ok, alarm */
    public String state;
    /* off, serve, guard */
    public String mode;
    public List<Sensor> sensors;

    public static class Sensor {
        public String name;
        public int state;
    }
}
