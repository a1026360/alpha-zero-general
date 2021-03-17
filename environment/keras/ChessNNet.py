import sys

from tensorflow.keras.models import *
from tensorflow.keras.layers import *
from tensorflow.keras.optimizers import *

sys.path.append('..')


class ChessNNet:
    def __init__(self, game, args):
        self.board_x, self.board_y = game.getBoardSize()
        self.action_size = game.getActionSize()
        self.args = args

        self.input_boards = Input(shape=(self.board_x, self.board_y))

        x_image = Reshape((self.board_x, self.board_y, 1))(self.input_boards)
        h_conv1 = Activation('relu')(BatchNormalization(axis=3)(
                Conv2D(32, (3, 3), padding='same')(x_image)))
        h_conv2 = Activation('relu')(BatchNormalization(axis=3)(
            Conv2D(32, (3, 3), padding='same')(h_conv1)))
        h_conv4 = Activation('relu')(BatchNormalization(axis=3)(
            Conv2D(64, (3, 3), strides=(2, 2), padding='valid')(h_conv2)))
        h_conv4_flat = Flatten()(h_conv4)
        s_fc1 = Activation('relu')(BatchNormalization(axis=1)(Dense(64)(h_conv4_flat)))
        self.pi = Dense(self.action_size, activation='softmax', name='pi')(s_fc1)
        self.v = Dense(1, activation='tanh', name='v')(s_fc1)

        self.model = Model(inputs=self.input_boards, outputs=[self.pi, self.v])
        self.model.compile(loss=['categorical_crossentropy', 'mean_squared_error'], optimizer=Adam(args.lr))
        print(self.model.summary())
