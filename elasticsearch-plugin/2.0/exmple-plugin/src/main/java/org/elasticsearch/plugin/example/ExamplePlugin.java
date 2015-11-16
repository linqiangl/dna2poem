package org.elasticsearch.plugin.example;

import org.elasticsearch.common.inject.Inject;
import org.elasticsearch.common.settings.Settings;
import org.elasticsearch.plugins.Plugin;
import org.elasticsearch.rest.RestModule;

public class ExamplePlugin extends Plugin {
    @Inject public ExamplePlugin(Settings settings) {
    }

    @Override public String name() {
        return "example-plugin";
    }

    @Override public String description() {
        return "Example Plugin Description";
    }

    public void onModule(RestModule module) {
        module.addRestAction(HelloRestHandler.class);
    }
}
