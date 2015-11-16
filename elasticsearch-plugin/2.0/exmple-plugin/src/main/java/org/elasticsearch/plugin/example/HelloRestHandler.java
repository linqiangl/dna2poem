package org.elasticsearch.plugin.example;

import org.elasticsearch.client.Client;
import org.elasticsearch.common.xcontent.XContentBuilder;
import org.elasticsearch.common.xcontent.json.JsonXContent;
import org.elasticsearch.common.inject.Inject;
import org.elasticsearch.common.settings.Settings;
import org.elasticsearch.rest.BaseRestHandler;
import org.elasticsearch.rest.RestController;
import org.elasticsearch.rest.RestRequest;
import org.elasticsearch.rest.RestChannel;
import org.elasticsearch.rest.RestRequest.Method;
import org.elasticsearch.rest.RestStatus;
import org.elasticsearch.rest.BytesRestResponse;


public class HelloRestHandler extends BaseRestHandler {
    @Inject
    public HelloRestHandler(Settings settings, Client client, RestController controller) {
        super(settings, controller, client);
        controller.registerHandler(Method.GET, "/_hello", this);
    }

    @Override
    public void handleRequest(RestRequest request, RestChannel channel, Client client) throws Exception {
        String who = request.param("who", null);
        if (who == null) who = "world";
        sendResponse(request, channel, who);
    }

    private void sendResponse(RestRequest request, RestChannel channel, String name) throws Exception {
        XContentBuilder builder = JsonXContent.contentBuilder();
        builder.startObject().field("say", "hello, " + name);
        builder.endObject();
        channel.sendResponse(new BytesRestResponse(RestStatus.OK, builder));
    }
}
